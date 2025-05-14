#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>


struct block {
    unsigned long int tag;
    int valid; // 0 means not used
    
    int used;  // for LRU
    
    int counter; // for FIFO
};

struct set {
    struct block* blocks;
    int size;
};

int main(int argc, char* argv[argc]) {
    
    if(argc < 6)
    {
        exit(1);
    }
    
    
    FILE* fp;
    fp=fopen(argv[8],"r");
    
    
    int cachesize=atoi(argv[1]);
    
    strtok(argv[2], ":");
    char* associativety_str = strtok(NULL, ":");
    int associativety=atoi(associativety_str);
    
    char* policy=argv[3];
    
    int blocksize=atoi(argv[4]);
    
    int l2cachesize=atoi(argv[5]);
    strtok(argv[6], ":");
    associativety_str = strtok(NULL, ":");
    int l2associativety=atoi(associativety_str);
    char* l2policy=argv[7];
    
    // L1 initialization
    int numsets = (cachesize/associativety) / (blocksize);
    
    struct set* sets = (struct set*)malloc(sizeof(struct set)*numsets);
    
    for(int i=0; i<numsets; i++)
    {
        sets[i].size = associativety;
        sets[i].blocks = (struct block*)malloc(sizeof(struct block)*associativety);
        
        for(int j=0; j<associativety; j++)
        {
            sets[i].blocks[j].valid=0;
            sets[i].blocks[j].used=0;
            sets[i].blocks[j].counter=0;
        }
    }
    
    // L2 initialization
    int l2numsets = (l2cachesize/l2associativety) / (blocksize);
    
    struct set* l2sets = (struct set*)malloc(sizeof(struct set)*l2numsets);
    
    for(int i=0; i<l2numsets; i++)
    {
        l2sets[i].size = l2associativety;
        l2sets[i].blocks = (struct block*)malloc(sizeof(struct block)*l2associativety);
        
        for(int j=0; j<l2associativety; j++)
        {
            l2sets[i].blocks[j].valid=0;
            l2sets[i].blocks[j].used=0;
            l2sets[i].blocks[j].counter=0;
        }
    }
    
    unsigned long int address;
    
    char oper;
    int reads=0;
    int writes=0;
    int hits=0;
    int misses=0;
    int l2hits=0;
    int l2misses=0; 
    int offsetbits= log(blocksize)/log(2);
    int setbits = log(numsets)/log(2);
    int l2setbits = log(l2numsets)/log(2);
    
    while(fscanf(fp, "%c %lx", &oper, &address)==2)
    {
        if(oper=='R')
        {
            //reads++;        
        }
        else
        {
            writes++;
        }
        //tagbits = address >> (offsetbits + setbits)
        address = address >> offsetbits;
        int set_num=0;
        if(setbits > 0)
        {
            unsigned long mask =0;
            for(int i=0; i<setbits; i++)
            {
                mask = (mask<<1) | 1;
            }
            
            set_num = address & mask;
        }
        
        unsigned long int tag = address >> setbits;

        int l2set_num=0;
        if(l2setbits > 0)
        {
            unsigned long mask =0;
            for(int i=0; i<l2setbits; i++)
            {
                mask = (mask<<1) | 1;
            }
            
            l2set_num = address & mask;
        }
        
        unsigned long int l2tag = address >> l2setbits;
        
        //struct set* targetset=sets[set_num];
        int found=0;
        int replaceblock=-1;
        int emptyblock=-1;
        int maxlru=-1;
        int maxfifo=-1;
        for(int i=0; i<sets[set_num].size; i++)
        {
            if(sets[set_num].blocks[i].valid == 1 && sets[set_num].blocks[i].tag==tag)
            {
                found=1;
                hits++;
                sets[set_num].blocks[i].used=0;
            }
            else if(sets[set_num].blocks[i].valid==0)
            {
                emptyblock=i;
            }
            else
            {
                // valid used block
                if(strcmp(policy, "lru")==0 && (maxlru==-1 || sets[set_num].blocks[i].used>maxlru))
                {
                    maxlru = sets[set_num].blocks[i].used;
                    replaceblock=i;
                }
                
                if(strcmp(policy, "fifo")==0 && (maxfifo==-1 || sets[set_num].blocks[i].counter > maxfifo))
                {
                    maxfifo = sets[set_num].blocks[i].counter;
                    replaceblock=i;
                }
                
                sets[set_num].blocks[i].used++;
            }
            if(sets[set_num].blocks[i].valid == 1)
            {
                sets[set_num].blocks[i].counter++;
            }
        }
        if(found==0)
        {
            // Did not find in L1
            misses++;
            //reads++;
            // search in L2
            int foundl2=0;
            int replaceblockl2=-1;
            for(int i=0; i<l2sets[l2set_num].size; i++)
            {
                if(l2sets[l2set_num].blocks[i].valid == 1 && l2sets[l2set_num].blocks[i].tag==l2tag)
                {
                    foundl2=1;
                    l2hits++;
                    l2sets[l2set_num].blocks[i].used=0;
                    replaceblockl2=i;
                }
                if(l2sets[l2set_num].blocks[i].valid == 1)
                {
                    l2sets[l2set_num].blocks[i].counter++;
                    l2sets[l2set_num].blocks[i].used++;
                }
            } 

            if(foundl2==1)
            {            
                l2sets[l2set_num].blocks[replaceblockl2].valid=0;
            }
            else
            {
              
                l2misses++;
                reads++;
            }
            
           // load into L1
            if(emptyblock!=-1)
            {
                 sets[set_num].blocks[emptyblock].tag = tag;
                 sets[set_num].blocks[emptyblock].valid=1;
                 sets[set_num].blocks[emptyblock].used=0;
                 sets[set_num].blocks[emptyblock].counter=0;
            }
            else
            {
                unsigned long temp = (sets[set_num].blocks[replaceblock].tag << setbits) | set_num;
                unsigned long l2newset_num=0;
                if(l2setbits > 0)
                {
                    unsigned long mask =0;
                    for(int i=0; i<l2setbits; i++)
                    {
                        mask = (mask<<1) | 1;
                    }
                        
                    l2newset_num = temp & mask;
                }
                    
                unsigned long newtag= temp >> l2setbits;
                int emptyblock2=-1;
                int replaceblock2=-1;
                maxlru=-1;
                maxfifo=-1;
                for(int i=0; i<l2sets[l2newset_num].size; i++)
                {
                    
                    if(l2sets[l2newset_num].blocks[i].valid==0)
                    {
                        emptyblock2=i;
                    }
                    else
                    {
                        // valid used block
                        if(strcmp(l2policy, "lru")==0 && (maxlru==-1 || l2sets[l2newset_num].blocks[i].used>maxlru))
                        {
                            maxlru = l2sets[l2newset_num].blocks[i].used;
                            replaceblock2=i;
                        }
                        
                        if(strcmp(l2policy, "fifo")==0 && (maxfifo==-1 || l2sets[l2newset_num].blocks[i].counter > maxfifo))
                        {
                            maxfifo = l2sets[l2newset_num].blocks[i].counter;
                            replaceblock2=i;
                        }
                        
                        l2sets[l2newset_num].blocks[i].used++;
                    }
                    if(l2sets[l2newset_num].blocks[i].valid == 1)
                     {
                        
                         l2sets[l2newset_num].blocks[i].counter++;
                     }
                    
                }
                
                if(emptyblock2!=-1)
                {
                    l2sets[l2newset_num].blocks[emptyblock2].tag = newtag;
                    l2sets[l2newset_num].blocks[emptyblock2].valid=1;
                    l2sets[l2newset_num].blocks[emptyblock2].used=0;
                    l2sets[l2newset_num].blocks[emptyblock2].counter=0;
                }
                else
                {
                    l2sets[l2newset_num].blocks[replaceblock2].tag = newtag;
                    l2sets[l2newset_num].blocks[replaceblock2].valid=1;
                    l2sets[l2newset_num].blocks[replaceblock2].used=0;
                    l2sets[l2newset_num].blocks[replaceblock2].counter=0;
                }

                sets[set_num].blocks[replaceblock].tag = tag;
                sets[set_num].blocks[replaceblock].valid=1;
                sets[set_num].blocks[replaceblock].used=0;
                sets[set_num].blocks[replaceblock].counter=0;
            }
        }

        getc(fp); // read the new line char
    }
            
    printf("memread: %d\n", reads);
    printf("memwrite: %d\n", writes);
    printf("l1cachehit: %d\n", hits);
    printf("l1cachemiss: %d\n", misses);
    printf("l2cachehit: %d\n", l2hits);
    printf("l2cachemiss: %d\n", l2misses);
    fclose(fp);
    
    for(int i=0; i<numsets; i++)
    {
        free(sets[i].blocks);
    }
    
    free(sets);
    
    
    for(int i=0; i<l2numsets; i++)
    {
        free(l2sets[i].blocks);
    }
    
    free(l2sets);
}

 //IF ITS NOT IN BOTH - if found 2 is still 0
            //check if theres an empty space in l1's correspinding set
            //if so put it and then ur done
            //if not do replacement policy and put it into the replaceblock and hold temp to put replaced block into l2
            //for putting it into l2, see if theres an empty space and if so put it in
            //if no empty space, remove using replacement policy and put it in

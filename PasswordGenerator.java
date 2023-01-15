import java.util.Scanner;
public class PasswordGenerator {
public static void main(String[] args) {
Scanner in = new Scanner(System.in);

System.out.print("Enter amount of passwords generated: ");
int amount = in.nextInt();
System.out.print("Enter how many characters long for each password: ");
int length = in.nextInt();

String[] RandPasswords = new String[amount];
for(int i = 0; i < amount; i++) {
    String randPassword = "";
    for(int j = 0; j < length; j++) {
        randPassword += randCharacter();
    }
     RandPasswords[i] = randPassword;
}
        print(RandPasswords);
}
public static void print(String[] arr) {
    for(int i = 0; i < arr.length; i++) {
        System.out.println(arr[i]);
    }
}

public static char randCharacter() {
    int rand = (int)(Math.random()*62);
    if(rand <= 9) {
        int ascii = rand + 48;
        return (char)(ascii);
    } else if(rand <= 35) {
        int ascii = rand + 55;
        return (char)(ascii);
    } else {
        int ascii = rand + 61;
        return (char)(ascii);
    }
}
}
    
 
n = readint();
fiblist = [1, 1];

if (n < 1 || n > 20) {
         print("Please enter a valid number between 1 and 20.");
} else if (n == 1) {
        print(fiblist[0:1]);
} else if (n == 2) {
        print(fiblist);
} else {
        i = 2;
        while (i < n) {
               next_fib = fiblist[i-1] + fiblist[i-2];
               fiblist = fiblist + [next_fib];
               i = i + 1;
               print(fiblist);
        }
 }

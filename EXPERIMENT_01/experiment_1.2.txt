class Solution {
public:
    double myPow(double x, int n) {
        long long N=n;
        double res=1;

        if(N<0){
            x=1/x;
            N=-N;
        }

       while(N>0){
        if(N & 1){
            res=res*x;
        }
        x=x*x;
        N=N>>1;
       }
       return res;
    }
};
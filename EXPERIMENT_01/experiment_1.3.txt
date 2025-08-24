class Solution {
public:
    vector<vector<int>> countFreq(vector<int>& arr) {
        int n=arr.size();
        
        sort(arr.begin(),arr.end());
        vector<vector<int>> res;
        
        int i=0;
        
        while(i<n) {
            int count=1;
            int j=i+1;
            while(j<n && arr[j]==arr[i]) {
                count++;
                j++;
            }
            res.push_back({arr[i],count});
            i=j;
        }
        return res;
    }
};
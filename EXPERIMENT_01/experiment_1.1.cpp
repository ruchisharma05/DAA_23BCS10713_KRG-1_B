#include <iostream>
using namespace std;

class St{
    public:

    int top= -1;
    int size;
    int* stack;
    St(int arr[],int n){
        size=n;
        stack=new int[n];
    }
    void push_element(int a){
        if(top==size-1){
            cout<<"Stack is Full\n";
            return;
        }
        top=top+1;
        stack[top]=a;
    }

    void pop_element(){
        if(top==-1){
            cout<<"Stack is Empty\n";
            return;
        }
        top=top-1;
    }

    void peek(){
        if(top==-1){
            cout<<"Stack is Empty\n";
            return;
        }
        cout<<stack[top]<<endl;
    }

    void isEmpty(){
        if(top==-1){
            cout<<"Stack is Empty\n";
        }else{
            cout<<"Stack is not Empty\n";
        }
    }

    void isFull(){
        if(top==size-1){
            cout<<"Stack is Full\n";
        }else{
            cout<<"Stack is not Full\n";
        }
    }

    void display(){
        if(top==-1){
            cout<<"Stack is Empty\n";
            return;
        }
        for(int i=0;i<=top;i++){
            cout<<stack[i]<<" ";
        }
        cout<<endl;
    }
};

int main(){
    int n;
    cin>>n;

    int arr[n];

    St obj(arr,n);
    
    obj.push_element(10);
    obj.push_element(3);
    obj.push_element(7);
    obj.pop_element();
    obj.peek();
    obj.isEmpty();
    obj.isFull();
    obj.display();
}

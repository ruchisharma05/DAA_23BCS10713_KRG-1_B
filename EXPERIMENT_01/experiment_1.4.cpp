#include <iostream>
using namespace std;

// Node structure for Doubly Linked List
struct Node {
    int data;
    Node* next;
    Node* prev;
    Node(int val){ 
        data=val; 
        next=prev=nullptr; }
};

// Doubly Linked List class
class DoublyLinkedList {
    Node* head;
public:
    DoublyLinkedList(){ 
        head = nullptr; 
    }
    
    void insertAtBeginning(int val){
        Node* newNode=new Node(val);
        if(!head){ 
            head=newNode; 
            return; 
        }
        newNode->next=head;
        head->prev=newNode;
        head=newNode;
    }
    
    void insertAtEnd(int val){
        Node* newNode=new Node(val);
        if(!head){ 
            head=newNode; 
            return; 
        }
        Node* temp=head;
        while(temp->next){
         temp=temp->next;
        }
        temp->next=newNode;
        newNode->prev=temp;
    }
    
    void deleteAtBeginning(){
        if(!head){ 
            return;
        }
        Node* temp=head;
        head=head->next;
        if(head){
            head->prev=nullptr;
        }
        delete temp;
    }
    
    void deleteAtEnd(){
        if(!head){ 
            return;
        }
        Node* temp=head;
        if(!temp->next){
             delete temp; 
             head=nullptr; 
             return; 
            }
        while(temp->next){
            temp=temp->next;
        }
        temp->prev->next=nullptr;
        delete temp;
    }
    
    void display(){
        Node* temp=head;
        while(temp){
             cout<<temp->data<<" "; 
             temp=temp->next; }
        cout<<endl;
    }
};

// Node structure for Circular Linked List
struct CNode {
    int data;
    CNode* next;
    CNode(int val){ 
        data=val; 
        next=this; }
};

// Circular Linked List class
class CircularLinkedList {
    CNode* tail;
public:
    CircularLinkedList(){ 
        tail = nullptr; 
    }
    
    void insertAtBeginning(int val){
        CNode* newNode=new CNode(val);
        if(!tail){ 
            tail=newNode; 
            return; 
        }
        newNode->next=tail->next;
        tail->next=newNode;
    }
    
    void insertAtEnd(int val){
        CNode* newNode=new CNode(val);
        if(!tail){ 
            tail=newNode; 
            return; 
        }
        newNode->next=tail->next;
        tail->next=newNode;
        tail=newNode;
    }
    
    void deleteAtBeginning(){
        if(!tail){
            return;
        }
        CNode* head=tail->next;
        if(head==tail){
             delete head; 
             tail=nullptr; 
             return; 
            }
        tail->next=head->next;
        delete head;
    }
    
    void deleteAtEnd(){
        if(!tail){
            return;
        }
        CNode* head=tail->next;
        if(head==tail){ 
            delete tail; 
            tail=nullptr; 
            return; 
        }
        CNode* temp=head;
        while(temp->next!=tail){
            temp=temp->next;
        }
        temp->next=tail->next;
        delete tail;
        tail=temp;
    }
    
    void display(){
        if(!tail){ 
            cout<<"List is empty\n"; 
            return; 
        }
        CNode* temp=tail->next;
        do{ 
            cout<<temp->data<<" "; 
            temp=temp->next; 
        }while(temp!=tail->next);
        cout<<endl;
    }
};

int main(){
    cout<<"Doubly Linked List:\n";
    DoublyLinkedList obj1;
    obj1.insertAtBeginning(10);
    obj1.insertAtEnd(20);
    obj1.insertAtBeginning(5);
    obj1.display();
    obj1.deleteAtBeginning();
    obj1.display();
    obj1.deleteAtEnd();
    obj1.display();

    cout<<"\nCircular Linked List:\n";
    CircularLinkedList obj2;
    obj2.insertAtBeginning(10);
    obj2.insertAtEnd(20);
    obj2.insertAtBeginning(5);
    obj2.display();
    obj2.deleteAtBeginning();
    obj2.display();
    obj2.deleteAtEnd();
    obj2.display();
}

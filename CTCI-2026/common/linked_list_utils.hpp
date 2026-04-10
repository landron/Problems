#pragma once

/*
The Risk: If the list is extremely long (e.g., 1 million nodes), the "chain
reaction" of destructors happens on the stack. This can cause a Stack Overflow
during the deletion process.
*/
struct Node {
    int data;
    std::unique_ptr<Node> next;
    Node(int d) : data(d), next(nullptr) {}
};

std::unique_ptr<Node> create_linked_list(std::initializer_list<int> values) {
    std::unique_ptr<Node> head;
    Node* tail = nullptr;
    for (int value : values) {
        auto new_node = std::make_unique<Node>(value);
        if (!head) {
            head = std::move(new_node);
            tail = head.get();
        } else {
            tail->next = std::move(new_node);
            tail = tail->next.get();
        }
    }
    return head;
}

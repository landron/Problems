#pragma once

/*
The Risk: If the list is extremely long (e.g., 1 million nodes), the "chain
reaction" of destructors happens on the stack. This can cause a Stack Overflow
during the deletion process.
*/
template <class T, typename PointerType = std::unique_ptr<void>>
struct GenericNode {
    // Conditional logic to determine the type of the 'next' member
    using NextPtr =
        std::conditional_t<std::is_same_v<PointerType, std::unique_ptr<void>>,
                           std::unique_ptr<GenericNode>, GenericNode*>;

    T val = {};
    NextPtr next;

    GenericNode() = default;
    GenericNode(T d, NextPtr next = nullptr) : val(d), next(std::move(next)) {}

    explicit operator T() const noexcept {
        return val;
    }
};

// Aliases to recreate your two specific node types clean and clear
template <class T>
using Node = GenericNode<T>; // Defaults to std::unique_ptr

template <class T>
using RawNode = GenericNode<T, void*>; // Configures 'next' to be a raw pointer

template <class T>
struct ListDeleter {
    void operator()(RawNode<T>* head) const {
        while (head) {
            auto nextNode = head->next;
            delete head;
            head = nextNode;
        }
    }
};

// Alias for convenience
template <class T>
using UniqueRawList = std::unique_ptr<RawNode<T>, ListDeleter<T>>;

//
//  Helpers
//

template <class T>
std::unique_ptr<Node<T>> create_linked_list(std::initializer_list<T> values) {
    std::unique_ptr<Node<T>> head;
    Node<T>* tail = nullptr;
    for (const auto& value : values) {
        auto new_node = std::make_unique<Node<T>>(value);
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

template <class T>
UniqueRawList<T> create_linked_list_raw(std::initializer_list<T> values) {
    RawNode<T>* head = nullptr;
    RawNode<T>* tail = nullptr;

    for (const auto& value : values) {
        auto* new_node = new RawNode<T>(value);
        if (!head) {
            head = new_node;
            tail = head;
        } else {
            tail->next = new_node;
            tail = tail->next;
        }
    }
    return UniqueRawList<T>(head);
}

// For standard Node (unique_ptr links)
template <class T>
std::vector<T> to_vector(const Node<T>* head) {
    std::vector<T> result;
    while (head) {
        result.push_back(head->val);
        head = head->next.get();
    }
    return result;
}

// For RawNode (raw pointer links)
template <class T>
std::vector<T> to_vector(const RawNode<T>* head) {
    std::vector<T> result;
    while (head) {
        result.push_back(head->val);
        head = head->next;
    }
    return result;
}

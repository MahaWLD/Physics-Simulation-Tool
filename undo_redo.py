class ActionNode:
    def __init__(self, action, data):
        self.action = action
        self.data = data
        self.next = None
        self.prev = None

# use 5 as max length - if list >= 5, pop list and then add action
# undo - move pointer down - so actions can be undone 5 times
# if pointer is at the bottom and action is added, move pointer to the action


class UndoRedoList:  # linked list
    def __init__(self):
        self.null_node = ActionNode(None, None)
        self.head = self.null_node
        self.current = self.null_node
        self.MAX_LENGTH = 5

    def append(self, action, data):
        new_node = ActionNode(action, data)  # aggregation

        if self.head is None:
            self.head = new_node
            self.current = new_node
        else:
            if self.len() >= self.MAX_LENGTH:
                self.delete_oldest()
            self.current.next = new_node  # swap
            new_node.prev = self.current
            self.current = new_node

    def len(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def delete_oldest(self):
        # check if list is empty
        if self.head is None:
            return

        oldest = self.head
        self.head = self.head.next  # make the second node the head
        if self.head:
            self.head.prev = None
        oldest.next = None  # remove reference to node

    def undo(self):
        if self.current and self.current.prev:  # if there is a previous node
            self.current = self.current.prev
            return self.current.next.action, self.current.next.data
        else:
            print("No action to undo")  # do nothing
            return None, None

    def redo(self):
        if self.current and self.current.next:  # if there is a node next
            self.current = self.current.next
            return self.current.action, self.current.data
        else:
            print("No action to redo")
            return None, None

    def display(self):  # not required
        current = self.head
        while current:
            print(current.action, current.data, end=" ")
            current = current.next
        print()

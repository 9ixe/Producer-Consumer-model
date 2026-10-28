# =====================================================================
# Program: Stack Implementation using List in Python
# Description: A menu-driven program demonstrating Push, Pop, Peek,
#              isEmpty, and Display operations with Underflow handling.
# Practical Exam Friendly (Basic Python)
# =====================================================================

def isEmpty(stack):
    """Checks whether the stack is empty."""
    return len(stack) == 0


def push(stack, item):
    """Adds an element to the top of the stack."""
    stack.append(item)
    print(f"Success: '{item}' pushed onto the stack.")


def pop(stack):
    """Removes and returns the top element of the stack."""
    if isEmpty(stack):
        print("Stack Underflow! The stack is empty. Cannot pop.")
        return None
    item = stack.pop()
    print(f"Success: Popped element is '{item}'.")
    return item


def peek(stack):
    """Displays the top element without removing it."""
    if isEmpty(stack):
        print("Stack Underflow! The stack is empty. Cannot peek.")
        return None
    top_element = stack[-1]
    print(f"Top element is: '{top_element}'")
    return top_element


def display(stack):
    """Displays all elements of the stack from top to bottom."""
    if isEmpty(stack):
        print("The stack is empty.")
    else:
        print("\n--- Current Stack (Top to Bottom) ---")
        for i in range(len(stack) - 1, -1, -1):
            if i == len(stack) - 1:
                print(f" {stack[i]}  <-- Top")
            else:
                print(f" {stack[i]}")
        print("-------------------------------------")


# ---------------------- Main Menu-Driven Logic ----------------------
def main():
    # Create an empty stack using a Python list
    stack = []

    while True:
        print("\n========== STACK OPERATIONS ==========")
        print("1. Push")
        print("2. Pop")
        print("3. Peek / Top")
        print("4. Display")
        print("5. Check if Empty (isEmpty)")
        print("6. Exit")
        print("======================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            item = input("Enter element to push: ").strip()
            push(stack, item)

        elif choice == '2':
            pop(stack)

        elif choice == '3':
            peek(stack)

        elif choice == '4':
            display(stack)

        elif choice == '5':
            if isEmpty(stack):
                print("Status: The stack is EMPTY.")
            else:
                print(f"Status: The stack is NOT empty (contains {len(stack)} item(s)).")

        elif choice == '6':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice! Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()

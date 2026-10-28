# Stack Implementation using List in Python

**Name:** Joel Biju
**UID:** 24003129
**Subject:** Operating Systems Practical

---

## Aim

To implement a stack using a Python list and perform the Push, Pop, Peek, Display and isEmpty operations through a menu-driven program, with underflow handling.

## Theory

A stack is a linear data structure that follows the **LIFO (Last In, First Out)** principle. Elements are added and removed from one end only, called the **top**. The element pushed last is the first one to be popped.

In Python, a list can act as a stack:

- `list.append(x)` adds an element at the top.
- `list.pop()` removes and returns the element at the top.
- `list[-1]` reads the top element without removing it.
- `len(list) == 0` tells whether the stack is empty.

Stacks are used in the operating system for function call management (call stack), context saving, expression evaluation and undo mechanisms.

### Operations

| Operation | Description | Time complexity |
|-----------|-------------|-----------------|
| Push | Adds an element to the top of the stack | O(1) |
| Pop | Removes and returns the top element | O(1) |
| Peek | Returns the top element without removing it | O(1) |
| isEmpty | Checks whether the stack has no elements | O(1) |
| Display | Prints all elements from top to bottom | O(n) |

### Underflow

Stack Underflow occurs when Pop or Peek is attempted on an empty stack. The program checks `isEmpty()` before these operations and prints an error message instead of failing.

## Algorithm

1. Create an empty list `stack`.
2. Display the menu and read the user's choice.
3. **Push:** read an element and append it to the list.
4. **Pop:** if the stack is empty, report underflow; otherwise remove and show the last element.
5. **Peek:** if the stack is empty, report underflow; otherwise show the last element without removing it.
6. **Display:** if the stack is empty, say so; otherwise print the elements from the last index down to index 0.
7. **isEmpty:** report whether the length of the list is zero.
8. **Exit:** end the program.
9. Repeat from step 2 until the user chooses Exit.

## Program

File: [`stack_implementation.py`](stack_implementation.py)

```python
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


def main():
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
```

## How to Run

Python 3.6 or later is required (the program uses f-strings).

```bash
python stack_implementation.py
```

## Sample Output

The menu is printed before every choice. It is shown in full once and left out of the later steps to keep this short.

```
========== STACK OPERATIONS ==========
1. Push
2. Pop
3. Peek / Top
4. Display
5. Check if Empty (isEmpty)
6. Exit
======================================
Enter your choice (1-6):
```

**Pop on an empty stack (underflow)**

```
Enter your choice (1-6): 2
Stack Underflow! The stack is empty. Cannot pop.
```

**Push**

```
Enter your choice (1-6): 1
Enter element to push: 10
Success: '10' pushed onto the stack.

Enter your choice (1-6): 1
Enter element to push: 20
Success: '20' pushed onto the stack.

Enter your choice (1-6): 1
Enter element to push: 30
Success: '30' pushed onto the stack.
```

**Display**

```
Enter your choice (1-6): 4

--- Current Stack (Top to Bottom) ---
 30  <-- Top
 20
 10
-------------------------------------
```

**Peek**

```
Enter your choice (1-6): 3
Top element is: '30'
```

**isEmpty**

```
Enter your choice (1-6): 5
Status: The stack is NOT empty (contains 3 item(s)).
```

**Pop**

```
Enter your choice (1-6): 2
Success: Popped element is '30'.
```

**Invalid choice**

```
Enter your choice (1-6): 9
Invalid choice! Please select an option from 1 to 6.
```

**Exit**

```
Enter your choice (1-6): 6
Exiting program. Goodbye!
```

## Result

The stack was implemented using a Python list. Push, Pop, Peek, Display and isEmpty work as expected, and Pop or Peek on an empty stack is handled with a Stack Underflow message.

---

## Simulator

File: [`stack_simulator.py`](stack_simulator.py)

The simulator runs all five operations automatically in a fixed sequence, without any user input. It uses the same `push`, `pop`, `peek`, `display` and `isEmpty` functions from the main program, so the logic is identical.

**Sequence of steps demonstrated:**

| Step | Operation | Expected result |
|------|-----------|-----------------|
| 1 | isEmpty | True (stack starts empty) |
| 2 | Pop | Stack Underflow |
| 3 | Peek | Stack Underflow |
| 4–7 | Push 10, 20, 30, 40 | Each element added to top |
| 8 | Display | 40 → 30 → 20 → 10 (top to bottom) |
| 9 | Peek | 40 |
| 10 | isEmpty | False |
| 11–14 | Pop × 4 | 40, 30, 20, 10 (LIFO order) |
| 15 | Display | Stack is empty |
| 16 | isEmpty | True |

A short delay (`DELAY = 0.6` seconds, adjustable at the top of the file) is added between steps so the output is easy to follow.

### How to Run

```bash
python stack_simulator.py
```

### Sample Output

```
=======================================================
       STACK SIMULATOR: OS PRACTICAL DEMONSTRATION
=======================================================
 Data structure : Stack (Python list)
 Operations     : Push, Pop, Peek, Display, isEmpty
 Underflow      : Triggered when Pop/Peek on empty stack
=======================================================

=============================================
  STEP: isEmpty  (stack is empty, expected: True)
=============================================
Stack is EMPTY.

=============================================
  STEP: Pop      (underflow expected)
=============================================
Stack Underflow! The stack is empty. Cannot pop.

=============================================
  STEP: Push     '10'
=============================================
Success: '10' pushed onto the stack.

=============================================
  STEP: Push     '20'
=============================================
Success: '20' pushed onto the stack.

=============================================
  STEP: Push     '30'
=============================================
Success: '30' pushed onto the stack.

=============================================
  STEP: Push     '40'
=============================================
Success: '40' pushed onto the stack.

=============================================
  STEP: Display  (4 elements)
=============================================

--- Current Stack (Top to Bottom) ---
 40  <-- Top
 30
 20
 10
-------------------------------------

=============================================
  STEP: Pop      (LIFO order)
=============================================
Success: Popped element is '40'.

=============================================
  STEP: Pop      (LIFO order)
=============================================
Success: Popped element is '30'.
```

---

Joel Biju | UID 24003129

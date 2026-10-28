# Producer-Consumer Problem (Smart Mall Tracking System)

**Name:** Joel Biju
**UID:** 24003129
**Subject:** Operating Systems Practical

---

## Aim

To implement the Producer-Consumer problem using threads and semaphores in Python, simulating a Smart Mall tracking system with a bounded buffer (conveyor belt), overflow handling, underflow handling, and garbage value rejection.

## Theory

The Producer-Consumer problem is a classic OS synchronisation problem where two processes share a fixed-size buffer:

- The **Producer** generates data and places it into the buffer.
- The **Consumer** reads data from the buffer and processes it.
- The **Buffer** has a fixed capacity (bounded buffer).

Three conditions must be handled:

| Condition | When it occurs | How it is handled |
|-----------|---------------|-------------------|
| Overflow | Producer tries to add when buffer is full | Producer blocks on `empty` semaphore |
| Underflow | Consumer tries to remove when buffer is empty | Consumer blocks on `full` semaphore |
| Garbage Value | Corrupted barcode, negative price, blank ID | Item rejected before entering the buffer |

### Semaphores Used

| Semaphore | Type | Initial Value | Purpose |
|-----------|------|---------------|---------|
| `empty` | Counting | `BUFFER_SIZE` (4) | Tracks number of free slots |
| `full` | Counting | 0 | Tracks number of filled slots |
| `mutex` | Binary (Lock) | 1 | Mutual exclusion for the critical section |

### Working

```
Producer:
  wait(empty)   → decrement free slots
  wait(mutex)   → enter critical section
    place item on belt
  signal(mutex) → exit critical section
  signal(full)  → increment filled slots

Consumer:
  wait(full)    → decrement filled slots
  wait(mutex)   → enter critical section
    remove item from belt
  signal(mutex) → exit critical section
  signal(empty) → increment free slots
```

## System Components

```
[RFID/Barcode Scanner]  →→→  [Conveyor Belt (4 slots)]  →→→  [Billing & Packing Station]
      PRODUCER                   BOUNDED BUFFER                      CONSUMER
```

| Component | Role |
|-----------|------|
| RFID / Barcode Scanner | Producer thread — scans items and places them on the belt |
| Conveyor Belt | Bounded buffer — holds up to `BUFFER_SIZE = 4` items |
| Billing & Packing Station | Consumer thread — removes and bills items from the belt |

## Algorithm

**Producer (Scanner):**
1. Validate the scanned item (check for garbage values).
2. If invalid, reject the item and discard it to the reject bin.
3. Call `wait(empty)` — block if no free slots available (overflow condition).
4. Call `wait(mutex)` — acquire the lock.
5. Place the item onto the conveyor belt (critical section).
6. Call `signal(mutex)` — release the lock.
7. Call `signal(full)` — notify the consumer that a new item is available.

**Consumer (Billing Station):**
1. Call `wait(full)` — block if no items are available (underflow condition).
2. Call `wait(mutex)` — acquire the lock.
3. Remove the first item from the conveyor belt, FIFO (critical section).
4. Call `signal(mutex)` — release the lock.
5. Call `signal(empty)` — notify the producer that a slot has freed up.
6. Print the billed item details.

**Garbage Value Check (`is_valid_item`):**
1. Reject if item ID or name is blank.
2. Reject if item ID contains corrupted barcode keywords (`ERR`, `CORRUPT`, `NULL`, etc.).
3. Reject if price is zero, negative, or non-numeric.
4. Reject if price exceeds Rs. 5,00,000 (sensor anomaly).

## Program

File: [`smart_mall_simulator.py`](smart_mall_simulator.py)

### Key Constants

```python
BUFFER_SIZE   = 4          # conveyor belt capacity
SCAN_DELAY    = (0.2, 0.6) # producer thread delay range (seconds)
BILLING_DELAY = (0.8, 1.6) # consumer thread delay range (seconds)
```

The scanner is faster than the billing station by design, so overflow events are triggered naturally during the simulation.

### Garbage Value Test Cases

| Test Case | Item ID | Price | Reason Rejected |
|-----------|---------|-------|-----------------|
| Damaged barcode | `ERR_CORRUPT_772` | 60 | Corrupt keyword in ID |
| Negative price | `ITEM_102` | -250 | Price must be greater than 0 |
| Non-numeric price | `ITEM_103` | `FREE_ITEM` | Price is not a number |
| Blank RFID tag | ` ` | 100 | ID and name cannot be blank |
| Unrealistic price | `MALL-099` | 90,00,000 | Sensor read anomaly |

## How to Run

Python 3.6 or later is required.

```bash
python smart_mall_simulator.py
```

The program asks for:
- **Number of items to scan** (default: 12)
- **Garbage item chance in %** (default: 20)

It then starts the producer and consumer as two separate threads and prints each event live.

## Sample Output

```
=======================================================
   SMART MALL TRACKING SYSTEM: PRODUCER-CONSUMER SIM
=======================================================
 Producer : RFID/Barcode Scanner (thread)
 Buffer   : Conveyor Belt (Capacity = 4 items)
 Consumer : Billing & Packing Station (thread)
=======================================================
Number of items to scan [12]: 8
Garbage (damaged) item chance in % [20]: 25

>>> Simulation started
    Items to scan: 8  |  Valid items: 6  |  Garbage: 2
    full=0 empty=4 | EMPTY | EMPTY | EMPTY | EMPTY

[SCANNER] GARBAGE VALUE REJECTED: Damaged/Corrupt barcode pattern detected in 'ERR_CORRUPT_772'.
    -> Item sent to reject bin. Belt unchanged.

[+] SUCCESS: Scanner placed 'Cereal Box' (ID: MALL-001, Rs.220.0) on belt.
    full=1 empty=3 | Cereal Box | EMPTY | EMPTY | EMPTY

[+] SUCCESS: Scanner placed 'Almond Milk' (ID: MALL-002, Rs.180.0) on belt.
    full=2 empty=2 | Cereal Box | Almond Milk | EMPTY | EMPTY

[*] PROCESSED & BILLED: 'Cereal Box' (ID: MALL-001)
    -> Item packed and billed for Rs. 220.00
    full=1 empty=3 | Almond Milk | EMPTY | EMPTY | EMPTY

[!] OVERFLOW ALERT: Conveyor belt is FULL. Scanner waiting...

[*] PROCESSED & BILLED: 'Almond Milk' (ID: MALL-002)
    -> Item packed and billed for Rs. 180.00
    full=0 empty=4 | EMPTY | EMPTY | EMPTY | EMPTY

>>> Simulation finished
    Placed on belt  : 6
    Rejected        : 2
    Billed          : 6
    Overflow events : 1
    Underflow events: 0
```

## Result

The Producer-Consumer problem was successfully simulated using Python threads and semaphores. The conveyor belt (bounded buffer) maintained synchronisation between the scanner (producer) and the billing station (consumer). Overflow was handled by blocking the producer, underflow by blocking the consumer, and garbage values were caught and rejected before reaching the buffer.

---

Joel Biju | UID 24003129

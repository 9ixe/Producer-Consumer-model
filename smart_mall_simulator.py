# ==============================================================================
# OS LAB: PRODUCER-CONSUMER SIMULATOR (SMART MALL TRACKING SYSTEM)
# ==============================================================================
# Producer : Scanner thread (RFID/Barcode scanner at billing gate)
# Buffer   : Conveyor belt, bounded buffer of BUFFER_SIZE slots
# Consumer : Billing & Packing thread (takes items off the belt)
#
# Semaphores:
#   empty  : counting semaphore, number of free slots   (starts at BUFFER_SIZE)
#   full   : counting semaphore, number of filled slots (starts at 0)
#   mutex  : binary lock, protects the conveyor belt critical section
# ==============================================================================

import threading
import time
import random

BUFFER_SIZE = 4

SCAN_DELAY = (0.2, 0.6)       # scanner takes this long (seconds) per item
BILLING_DELAY = (0.8, 1.6)    # billing station takes this long per item

conveyor_belt = []
mutex = threading.Lock()
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
print_lock = threading.Lock()

stats = {"placed": 0, "rejected": 0, "billed": 0, "overflow": 0, "underflow": 0}

SAMPLE_ITEMS = [
    ("MALL-001", "Cereal Box", "220"),
    ("MALL-002", "Almond Milk", "180"),
    ("MALL-003", "Olive Oil", "550"),
    ("MALL-004", "Brown Bread", "50"),
    ("MALL-005", "Extra Jam", "120"),
    ("MALL-006", "Organic Apples", "150"),
    ("MALL-007", "Juice Bottle", "95"),
]

GARBAGE_ITEMS = [
    ("ERR_CORRUPT_772", "Milk Packet", "60"),
    ("ITEM_102", "Chocolate Bar", "-250"),
    ("ITEM_103", "Juice Bottle", "FREE_ITEM"),
    ("", "", "100"),
    ("MALL-099", "Gold Bar", "9000000"),
]


def is_valid_item(item_id, item_name, price):
    """
    Validates item data to prevent GARBAGE VALUES from entering the system.
    Returns: (bool, str) -> (is_valid, error_reason)
    """
    if not item_id or not item_name:
        return False, "Item ID and Item Name cannot be blank."

    garbage_keywords = ["ERR", "CORRUPT", "NULL", "UNDEFINED", "???"]
    if any(keyword in item_id.upper() for keyword in garbage_keywords):
        return False, f"Damaged/Corrupt barcode pattern detected in '{item_id}'."

    try:
        price_val = float(price)
        if price_val <= 0:
            return False, f"Invalid price '{price}'. Price must be greater than 0."
        if price_val > 500000:
            return False, f"Unrealistic price '{price}'. Sensor read anomaly."
    except ValueError:
        return False, f"Price '{price}' is not a valid number."

    return True, "Valid"


def log(message):
    with print_lock:
        print(message)


def belt_status():
    with mutex:
        count = len(conveyor_belt)
        slots = []
        for i in range(BUFFER_SIZE):
            if i < count:
                slots.append(conveyor_belt[i]["name"][:12])
            else:
                slots.append("EMPTY")
    return f"full={count} empty={BUFFER_SIZE - count} | " + " | ".join(slots)


def scanner_produce(item_id, item_name, price):
    """
    PRODUCER: scans one item and places it on the conveyor belt.
    Blocks on the 'empty' semaphore when the belt is full (OVERFLOW).
    """
    valid, reason = is_valid_item(item_id, item_name, price)
    if not valid:
        with mutex:
            stats["rejected"] += 1
        log(f"[SCANNER] GARBAGE VALUE REJECTED: {reason}")
        log("    -> Item sent to reject bin. Belt unchanged.")
        return

    # wait(empty)
    if not empty.acquire(blocking=False):
        with mutex:
            stats["overflow"] += 1
        log("[!] OVERFLOW ALERT: Conveyor belt is FULL. Scanner waiting...")
        empty.acquire()

    # critical section
    item = {
        "id": item_id.strip(),
        "name": item_name.strip(),
        "price": float(price),
    }
    with mutex:
        conveyor_belt.append(item)
        stats["placed"] += 1
    # signal(full)
    full.release()

    log(f"[+] SUCCESS: Scanner placed '{item['name']}' (ID: {item['id']}, Rs.{item['price']}) on belt.")
    log("    " + belt_status())


def billing_consume():
    """
    CONSUMER: takes one item off the belt, FIFO.
    Blocks on the 'full' semaphore when the belt is empty (UNDERFLOW).
    """
    # wait(full)
    if not full.acquire(blocking=False):
        with mutex:
            stats["underflow"] += 1
        log("[!] UNDERFLOW ALERT: Conveyor belt is EMPTY. Billing station waiting...")
        full.acquire()

    # critical section
    with mutex:
        item = conveyor_belt.pop(0)
        stats["billed"] += 1
    # signal(empty)
    empty.release()

    log(f"[*] PROCESSED & BILLED: '{item['name']}' (ID: {item['id']})")
    log(f"    -> Item packed and billed for Rs. {item['price']:.2f}")
    log("    " + belt_status())


def scanner_thread(items):
    for item_id, item_name, price in items:
        time.sleep(random.uniform(*SCAN_DELAY))
        scanner_produce(item_id, item_name, price)


def billing_thread(total_valid):
    for _ in range(total_valid):
        time.sleep(random.uniform(*BILLING_DELAY))
        billing_consume()


def build_items(count, garbage_pct):
    items = []
    for _ in range(count):
        if random.randint(1, 100) <= garbage_pct:
            items.append(random.choice(GARBAGE_ITEMS))
        else:
            items.append(random.choice(SAMPLE_ITEMS))
    return items


def display_conveyor_belt():
    print("\n" + "=" * 55)
    print("        SMART MALL CONVEYOR BELT (SHARED BUFFER)       ")
    print("=" * 55)
    print(" Capacity: " + str(BUFFER_SIZE) + " slots")
    print(" " + belt_status())
    print("-" * 55)
    with mutex:
        for idx in range(BUFFER_SIZE):
            if idx < len(conveyor_belt):
                item = conveyor_belt[idx]
                print(f" Slot [{idx + 1}]: {item['name']:<18} | ID: {item['id']:<10} | Rs. {item['price']}")
            else:
                print(f" Slot [{idx + 1}]: [ EMPTY SLOT ]")
    print("=" * 55)


def main():
    print("=======================================================")
    print("   SMART MALL TRACKING SYSTEM: PRODUCER-CONSUMER SIM   ")
    print("=======================================================")
    print(" Producer : RFID/Barcode Scanner (thread)")
    print(" Buffer   : Conveyor Belt (Capacity = " + str(BUFFER_SIZE) + " items)")
    print(" Consumer : Billing & Packing Station (thread)")
    print("=======================================================")

    count_text = input("Number of items to scan [12]: ").strip()
    count = int(count_text) if count_text else 12

    garbage_text = input("Garbage (damaged) item chance in % [20]: ").strip()
    garbage_pct = int(garbage_text) if garbage_text else 20

    items = build_items(count, garbage_pct)
    total_valid = sum(1 for it in items if is_valid_item(*it)[0])

    print("\n>>> Simulation started")
    print(f"    Items to scan: {count}  |  Valid items: {total_valid}  |  Garbage: {count - total_valid}")
    print("    " + belt_status())

    producer = threading.Thread(target=scanner_thread, args=(items,))
    consumer = threading.Thread(target=billing_thread, args=(total_valid,))

    producer.start()
    consumer.start()
    producer.join()
    consumer.join()

    print("\n>>> Simulation finished")
    print(f"    Placed on belt : {stats['placed']}")
    print(f"    Rejected       : {stats['rejected']}")
    print(f"    Billed         : {stats['billed']}")
    print(f"    Overflow events : {stats['overflow']}")
    print(f"    Underflow events: {stats['underflow']}")
    display_conveyor_belt()


if __name__ == "__main__":
    main()

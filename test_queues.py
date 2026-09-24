"""ITECC04 Laboratory 4, Part D: checks for the circular queue and the deque.

Run:  python3 test_queues.py

If your Part D file is not named queues.py, change the import line below to
match your actual filename.
"""

from queues import CircularQueue, Deque, is_palindrome

passed = 0
failed = 0
unwritten = 0


def check(label, expected, produce):
    """Runs one check and prints one line."""
    global passed, failed, unwritten
    try:
        actual = produce()
    except NotImplementedError as unfinished:
        unwritten += 1
        print(f"  [ ] {label}  <- not written yet: {unfinished}")
        return
    except Exception as error:
        failed += 1
        print(f"  [X] {label}  <- {type(error).__name__}: {error}")
        return
    if actual == expected:
        passed += 1
        print(f"  [OK] {label}")
    else:
        failed += 1
        print(f"  [X] {label}  <- expected {expected!r}, got {actual!r}")


def check_raises(label, error_type, produce):
    """Passes only when the named error is raised."""
    global passed, failed, unwritten
    try:
        produce()
    except NotImplementedError as unfinished:
        unwritten += 1
        print(f"  [ ] {label}  <- not written yet: {unfinished}")
        return
    except error_type:
        passed += 1
        print(f"  [OK] {label}")
        return
    except Exception as error:
        failed += 1
        print(f"  [X] {label}  <- raised {type(error).__name__}, wanted "
              f"{error_type.__name__}")
        return
    failed += 1
    print(f"  [X] {label}  <- nothing was raised, wanted {error_type.__name__}")


# ---------------------------------------------------------------------------
# CircularQueue
# ---------------------------------------------------------------------------

print("ITECC04 Laboratory 4, Part D: CircularQueue")

check("a new queue is empty", True, lambda: CircularQueue(3).is_empty())
check("a new queue is not full", False, lambda: CircularQueue(3).is_full())
check("a new queue has size 0", 0, lambda: CircularQueue(3).size())
check_raises("capacity 0 raises ValueError", ValueError,
             lambda: CircularQueue(0))


def enqueue_raises_size():
    q = CircularQueue(3)
    q.enqueue("a")
    return q.size()
check("enqueue raises the size to 1", 1, enqueue_raises_size)


def peek_returns_first():
    q = CircularQueue(3)
    q.enqueue("a")
    q.enqueue("b")
    return q.peek()
check("peek returns the first item enqueued", "a", peek_returns_first)


def peek_leaves_size():
    q = CircularQueue(3)
    q.enqueue("a")
    q.peek()
    q.peek()
    return q.size()
check("peek leaves the size alone", 1, peek_leaves_size)


def fifo_order():
    q = CircularQueue(3)
    for item in [1, 2, 3]:
        q.enqueue(item)
    return [q.dequeue(), q.dequeue(), q.dequeue()]
check("items leave in the order they arrived", [1, 2, 3], fifo_order)


def full_queue():
    q = CircularQueue(2)
    q.enqueue("a")
    q.enqueue("b")
    return q.is_full()
check("filling to capacity reports full", True, full_queue)


def overflow():
    q = CircularQueue(2)
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
check_raises("enqueue on a full queue raises OverflowError", OverflowError,
             overflow)

check_raises("dequeue on an empty queue raises IndexError", IndexError,
             lambda: CircularQueue(2).dequeue())
check_raises("peek on an empty queue raises IndexError", IndexError,
             lambda: CircularQueue(2).peek())

print("\nwraparound: the slot freed at the front must be reused")


def wrap_slots():
    q = CircularQueue(4)
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    q.enqueue("D")
    q.dequeue()          # removes A, clears slot 0
    q.dequeue()          # removes B, clears slot 1
    q.enqueue("E")        # wraps around to slot 0
    return q.slots()
check("slots read ['E', None, 'C', 'D'] after wrapping",
      ["E", None, "C", "D"], wrap_slots)


def wrap_order():
    q = CircularQueue(4)
    for item in ["A", "B", "C", "D"]:
        q.enqueue(item)
    q.dequeue()
    q.dequeue()
    q.enqueue("E")
    return [q.dequeue(), q.dequeue(), q.dequeue()]
check("wrapped items still leave in order", ["C", "D", "E"], wrap_order)


def stress_wrap():
    q = CircularQueue(3)
    last = None
    for i in range(30):
        q.enqueue(i)
        last = q.dequeue()
    return last
check("30 enqueue and dequeue pairs on a capacity of 3", 29, stress_wrap)


def cleared_slot():
    q = CircularQueue(2)
    q.enqueue("a")
    q.dequeue()
    return q.slots()
check("a dequeued slot is cleared to None", [None, None], cleared_slot)


# ---------------------------------------------------------------------------
# Deque
# ---------------------------------------------------------------------------

print("\nITECC04 Laboratory 4, Part D: Deque")

check("a new deque is empty", True, lambda: Deque().is_empty())


def add_remove_both_ends():
    d = Deque()
    d.add_rear(1)
    d.add_rear(2)
    d.add_front(0)
    # deque is now: 0, 1, 2
    return [d.remove_front(), d.remove_rear(), d.remove_front()]
check("add and remove at both ends", [0, 2, 1], add_remove_both_ends)


def size_tracks_both_ends():
    d = Deque()
    d.add_front("a")
    d.add_rear("b")
    d.remove_front()
    return d.size()
check("size tracks both ends", 1, size_tracks_both_ends)

check_raises("remove_front on empty raises IndexError", IndexError,
             lambda: Deque().remove_front())
check_raises("remove_rear on empty raises IndexError", IndexError,
             lambda: Deque().remove_rear())


# ---------------------------------------------------------------------------
# is_palindrome
# ---------------------------------------------------------------------------

print("\nis_palindrome")

check("'radar' is a palindrome", True, lambda: is_palindrome("radar"))
check("'Level' ignores case", True, lambda: is_palindrome("Level"))
check("'A man, a plan, a canal: Panama' ignores punctuation",
      True, lambda: is_palindrome("A man, a plan, a canal: Panama"))
check("'stack' is not a palindrome", False, lambda: is_palindrome("stack"))
check("'noon' has even length", True, lambda: is_palindrome("noon"))
check("a single letter is a palindrome", True, lambda: is_palindrome("a"))
check("an empty string is a palindrome", True, lambda: is_palindrome(""))


print()
print("=" * 60)
print(f"passed {passed}   failed {failed}   not written yet {unwritten}")
if unwritten:
    print("Write the steps named above, then run this file again.")
elif failed == 0:
    print("Part D is finished. The queue wraps, and the deque works from both ends.")
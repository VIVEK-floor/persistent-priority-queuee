import os
import unittest

from module import PersistentPriorityQueue


TEST_FILE = "test_data.json"


class TestPersistentPriorityQueue(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

        self.queue = PersistentPriorityQueue(TEST_FILE)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_insert(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")

        self.assertEqual(len(self.queue.heap), 2)
        self.assertEqual(self.queue.peek("min")["priority"], 1)

    def test_extract_min(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")
        self.queue.insert("Task C", 3, "task-3")

        result = self.queue.extract_min()

        self.assertEqual(result["id"], "task-2")
        self.assertEqual(result["priority"], 1)

    def test_extract_max(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")
        self.queue.insert("Task C", 3, "task-3")

        result = self.queue.extract_max()

        self.assertEqual(result["id"], "task-1")
        self.assertEqual(result["priority"], 5)

    def test_peek(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")
        self.queue.insert("Task C", 3, "task-3")

        minimum = self.queue.peek("min")
        maximum = self.queue.peek("max")

        self.assertEqual(minimum["priority"], 1)
        self.assertEqual(maximum["priority"], 5)

        # peek must not remove anything
        self.assertEqual(len(self.queue.heap), 3)

    def test_update(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")
        self.queue.insert("Task C", 3, "task-3")

        result = self.queue.update("task-3", 0)

        self.assertEqual(result["priority"], 0)
        self.assertEqual(self.queue.peek("min")["id"], "task-3")

    def test_delete(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")

        result = self.queue.delete("task-1")

        self.assertEqual(result["id"], "task-1")
        self.assertEqual(len(self.queue.heap), 1)

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())

        self.queue.insert("Task A", 1, "task-1")

        self.assertFalse(self.queue.is_empty())

    def test_persistence(self):
        self.queue.insert("Task A", 5, "task-1")
        self.queue.insert("Task B", 1, "task-2")

        # Create a new queue using the same storage file
        new_queue = PersistentPriorityQueue(TEST_FILE)

        self.assertEqual(len(new_queue.heap), 2)
        self.assertEqual(new_queue.peek("min")["id"], "task-2")


if __name__ == "__main__":
    unittest.main()
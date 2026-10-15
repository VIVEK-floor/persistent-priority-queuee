import uuid

from storage import Storage


class PersistentPriorityQueue:

    def __init__(self, storage_file="data.json"):
        self.storage = Storage(storage_file)
        self.heap = []

        self._load_data()

    def _load_data(self):
        data = self.storage.load()
        self.heap = data
        self._build_heap()

    def _save_data(self):
        self.storage.save(self.heap)

    def _build_heap(self):
        for index in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(index)

    def _heapify_down(self, index):
        size = len(self.heap)

        while True:
            smallest = index

            left = 2 * index + 1
            right = 2 * index + 2

            if (
                left < size
                and self.heap[left]["priority"]
                < self.heap[smallest]["priority"]
            ):
                smallest = left

            if (
                right < size
                and self.heap[right]["priority"]
                < self.heap[smallest]["priority"]
            ):
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = (
                self.heap[smallest],
                self.heap[index],
            )

            index = smallest

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if (
                self.heap[index]["priority"]
                >= self.heap[parent]["priority"]
            ):
                break

            self.heap[index], self.heap[parent] = (
                self.heap[parent],
                self.heap[index],
            )

            index = parent

    def insert(self, value, priority, item_id=None):
        if item_id is None:
            item_id = str(uuid.uuid4())

        item = {
            "id": item_id,
            "value": value,
            "priority": priority
        }

        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
        self._save_data()

        return item

    def extract_min(self):
        if self.is_empty():
            return None

        min_item = self.heap[0]

        last_item = self.heap.pop()

        if self.heap:
            self.heap[0] = last_item
            self._heapify_down(0)

        self._save_data()

        return min_item


    def is_empty(self):
        return len(self.heap) == 0

    def extract_max(self):
        if self.is_empty():
            return None

        max_index = 0

        for index in range(1, len(self.heap)):
            if self.heap[index]["priority"] > self.heap[max_index]["priority"]:
                max_index = index

        max_item = self.heap[max_index]

        last_item = self.heap.pop()

        if max_index < len(self.heap):
            self.heap[max_index] = last_item

            parent = (max_index - 1) // 2

            if (
                max_index > 0
                and self.heap[max_index]["priority"]
                < self.heap[parent]["priority"]
            ):
                self._heapify_up(max_index)
            else:
                self._heapify_down(max_index)

        self._save_data()

        return max_item


    def peek(self, mode="min"):
        if self.is_empty():
            return None

        if mode == "min":
            return self.heap[0]

        if mode == "max":
            max_item = self.heap[0]

            for item in self.heap[1:]:
                if item["priority"] > max_item["priority"]:
                    max_item = item

            return max_item

        raise ValueError("mode must be 'min' or 'max'")

    def update(self, item_id, new_priority):
        for index, item in enumerate(self.heap):

            if item["id"] == item_id:

                old_priority = item["priority"]
                item["priority"] = new_priority

                if new_priority < old_priority:
                    self._heapify_up(index)
                elif new_priority > old_priority:
                    self._heapify_down(index)

                self._save_data()

                return item

        return None
    def delete(self, item_id):
        for index, item in enumerate(self.heap):

            if item["id"] == item_id:

                deleted_item = self.heap[index]

                last_item = self.heap.pop()

                if index < len(self.heap):
                    self.heap[index] = last_item

                    parent = (index - 1) // 2

                    if (
                        index > 0
                        and self.heap[index]["priority"]
                        < self.heap[parent]["priority"]
                    ):
                        self._heapify_up(index)
                    else:
                        self._heapify_down(index)

                self._save_data()

                return deleted_item

        return None




# if __name__ == "__main__":
#     queue = PersistentPriorityQueue()

#     queue.insert("Fix login bug", 1, "task-001")
#     queue.insert("Update documentation", 5, "task-002")
#     queue.insert("Deploy application", 3, "task-003")

#     print("Before delete:")
#     print(queue.heap)

#     result = queue.delete("task-002")

#     print("\nDeleted item:")
#     print(result)

#     print("\nAfter delete:")
#     print(queue.heap)
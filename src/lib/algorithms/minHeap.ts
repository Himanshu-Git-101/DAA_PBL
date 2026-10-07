/**
 * Binary Min-Heap Priority Queue
 * Implemented from scratch without external libraries.
 * Stores { priority: number, item: T } where lowest priority is at root (index 0).
 * Time Complexity: Push O(log n), Pop O(log n), Peek O(1).
 */
export interface HeapEntry<T> {
  priority: number;
  item: T;
}

export class MinHeapPriorityQueue<T = string> {
  private heap: Array<HeapEntry<T>> = [];

  constructor() {
    this.heap = [];
  }

  isEmpty(): boolean {
    return this.heap.length === 0;
  }

  size(): number {
    return this.heap.length;
  }

  peek(): HeapEntry<T> | undefined {
    return this.heap[0];
  }

  push(priority: number, item: T): void {
    this.heap.push({ priority, item });
    this.siftUp(this.heap.length - 1);
  }

  pop(): HeapEntry<T> {
    if (this.isEmpty()) {
      throw new Error("Cannot pop from an empty priority queue.");
    }
    const min = this.heap[0];
    const last = this.heap.pop()!;
    if (!this.isEmpty()) {
      this.heap[0] = last;
      this.siftDown(0);
    }
    return min;
  }

  private siftUp(idx: number): void {
    let parent = Math.floor((idx - 1) / 2);
    while (idx > 0 && this.heap[idx].priority < this.heap[parent].priority) {
      this.swap(idx, parent);
      idx = parent;
      parent = Math.floor((idx - 1) / 2);
    }
  }

  private siftDown(idx: number): void {
    const size = this.heap.length;
    while (true) {
      const left = 2 * idx + 1;
      const right = 2 * idx + 2;
      let smallest = idx;

      if (left < size && this.heap[left].priority < this.heap[smallest].priority) {
        smallest = left;
      }
      if (right < size && this.heap[right].priority < this.heap[smallest].priority) {
        smallest = right;
      }

      if (smallest !== idx) {
        this.swap(idx, smallest);
        idx = smallest;
      } else {
        break;
      }
    }
  }

  private swap(i: number, j: number): void {
    const temp = this.heap[i];
    this.heap[i] = this.heap[j];
    this.heap[j] = temp;
  }

  getElements(): Array<HeapEntry<T>> {
    return [...this.heap];
  }
}

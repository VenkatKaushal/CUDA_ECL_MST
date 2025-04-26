import struct
import sys
from collections import defaultdict

def convert_snap_to_el(txt_file, el_file):
    print(f"Reading edge list from: {txt_file}")

    edges_set = set()
    max_node = -1

    
    with open(txt_file, 'r') as f:
        for line in f:
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            u, v = map(int, line.strip().split())
            if u == v:
                continue  
            edges_set.add((u, v))
            edges_set.add((v, u))  
            max_node = max(max_node, u, v)

    nodes = max_node + 1
    adj = defaultdict(list)

    for u, v in edges_set:
        adj[u].append(v)

    # Build CSR (Compressed Sparse Row) format
    nindex = [0]
    nlist = []
    eweight = []

    for i in range(nodes):
        neighbors = adj[i]
        nlist.extend(neighbors)
        eweight.extend([1] * len(neighbors)) 
        nindex.append(len(nlist))

    edges = len(nlist)

    print(f"Writing .el file: {el_file}")
    print(f"Nodes: {nodes}, Edges: {edges}")

    with open(el_file, "wb") as f:
        f.write(struct.pack('i', nodes))
        f.write(struct.pack('i', edges))
        f.write(struct.pack('i' * len(nindex), *nindex))
        f.write(struct.pack('i' * len(nlist), *nlist))
        f.write(struct.pack('i' * len(eweight), *eweight))

    print("Conversion complete!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_snap_to_el.py input.txt output.el")
        sys.exit(1)
    convert_snap_to_el(sys.argv[1], sys.argv[2])
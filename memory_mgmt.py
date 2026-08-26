"""
memory_mgmt.py

Implements mathematical physical memory address translations.
Evaluates both Paging (with Page Faulting) and Segmentation (with Bounds Checking).
"""

# Hardcoded environment parameters required by the PRD constraints
PAGE_SIZE = 1024
PAGE_TABLE = {0: 5, 1: 2, 2: 9, 3: 1}
SEGMENT_TABLE = {0: (1000, 400), 1: (2200, 300), 2: (500, 150)} # {segment: (base, limit)}

def translate_page(logical_address):
    """Translates a contiguous logical paged address into actual physical frame mappings."""
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE
    
    if page_number not in PAGE_TABLE:
        return f"Addr {logical_address:<4} -> PAGE FAULT! (Page {page_number} is unregistered in mapping table)"
        
    frame_number = PAGE_TABLE[page_number]
    phys_addr = (frame_number * PAGE_SIZE) + offset
    return f"Addr {logical_address:<4} -> Page {page_number}, Offset {offset:<4} ==> Physical: {phys_addr}"


def translate_segment(segment_tuple):
    """Executes bounds-checking and physical translation for segmented execution boundaries."""
    segment, offset = segment_tuple
    
    if segment not in SEGMENT_TABLE:
        return f"Tuple {str(segment_tuple):<8} -> INVALID SEGMENT!"
        
    base, limit = SEGMENT_TABLE[segment]
    
    # Critical OS bounds checking to prevent illegal contiguous access
    if offset >= limit:
        return f"Tuple {str(segment_tuple):<8} -> SEGMENTATION FAULT! (Offset {offset} exceeds limit {limit})"
        
    phys_addr = base + offset
    return f"Tuple {str(segment_tuple):<8} -> Base {base} + Offset {offset:<3} ==> Physical: {phys_addr}"


if __name__ == "__main__":
    print("\n=========== PAGING MMU SIMULATION ===========")
    paged_addresses = [260, 1500, 3000, 5000]
    for address in paged_addresses:
        print(translate_page(address))
        
    print("\n======== SEGMENTATION MMU SIMULATION ========")
    segmented_addresses = [(0, 150), (1, 350), (2, 100)]
    for address_tuple in segmented_addresses:
        print(translate_segment(address_tuple))

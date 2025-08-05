import uproot
import awkward as ak
import numpy as np

def filter_file(path, output_path):
    try:
        file = uproot.open(path)
        tree = file["tree"]

        # Load label arrays into a dict
        label_arrays = {field: tree[field].array(library="ak") for field in label_fields}

        num_entries = len(next(iter(label_arrays.values())))
        if num_entries == 0:
            return f"📂 {path}\n⚠️  No events found — skipping."

        # Stack labels per event
        labels_stacked = ak.Array([
            [label_arrays[field][i] for field in label_fields]
            for i in range(num_entries)
        ])

        # Create a mask where exactly one label is set per event
        label_counts = ak.sum(labels_stacked, axis=1)
        mask = (label_counts == 1)

        n_kept = ak.sum(mask)
        n_dropped = num_entries - n_kept

        if n_kept == 0:
            return f"📂 {path}\n⚠️  No clean events found after filtering."

        # Now filter all branches by the mask
        # We'll filter all arrays in the tree that are not just the labels, to keep complete events
        all_branches = tree.keys()
        arrays = {branch: tree[branch].array(library="ak") for branch in all_branches}
        arrays_filtered = {branch: arrays[branch][mask] for branch in all_branches}

        # Write filtered arrays to a new ROOT file
        with uproot.recreate(output_path) as new_file:
            new_file["tree"] = arrays_filtered

        return (f"📂 {path}\n✅ Filtered file saved to {output_path}\n"
                f"Kept {n_kept} events, dropped {n_dropped} events with mixed labels.")

    except KeyError as e:
        return f"📂 {path}\n⚠️  Missing field: {e}"
    except Exception as e:
        return f"📂 {path}\n💥 Unexpected error: {e}"


# Example usage in parallel (you can adapt your existing code to call filter_file):
if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor, as_completed

    output_paths = [p.replace(".root", "_filtered.root") for p in paths]

    print("🔄 Filtering files in parallel...\n")

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(filter_file, path, out) for path, out in zip(paths, output_paths)]
        for future in as_completed(futures):
            print(future.result())

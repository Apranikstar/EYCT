import uproot
import awkward as ak
from concurrent.futures import ThreadPoolExecutor, as_completed

label_fields = [
    "process_isHLNUQQ", "process_isHQQLNU", "process_isENUEQQ", "process_isEEQQ",
    "process_isMUNUMUQQ", "process_isMUMUQQ", "process_isTAUNUTAUQQ", "process_isTAUTAUQQ",
    "process_isHTAUTAU", "process_isHLLNUNU", "process_isEENUNU", "process_isMUMUNUNU",
    "process_isTAUTAUNUNU", "process_isL1L2NUNU", "process_isTAUTAU", "process_isHGG",
    "process_isHBB", "process_isQQ"
]

paths = [
    "/home/apranik/workingSpace/EYCT/data/stage2_Hbb.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_Hgg.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_Hllnunu.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_Hlnuqq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_Hqqlnu.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_Htautau.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_eenunu.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_eeqq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_enueqq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_l1l2nunu.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_mumuqq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_munumuqq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_qq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_taunutauqq.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_tautau.root",
    "/home/apranik/workingSpace/EYCT/data/stage2_tautaununu.root"
]


def check_file(path):
    try:
        file = uproot.open(path)
        tree = file["tree"]

        # Read all label arrays
        label_arrays = {field: tree[field].array() for field in label_fields}

        num_entries = len(next(iter(label_arrays.values())))
        if num_entries == 0:
            return f"📂 {path}\n⚠️  No events found — skipping."

        # Stack the label fields per event
        labels_stacked = ak.Array([
            [label_arrays[field][i] for field in label_fields]
            for i in range(num_entries)
        ])

        if len(labels_stacked) == 0:
            return f"📂 {path}\n⚠️  Empty label array — skipping."

        # Count how many labels are set to 1 per event
        label_counts = ak.sum(labels_stacked, axis=1)
        n_conflicts = ak.sum(label_counts > 1)

        if n_conflicts > 0:
            return f"📂 {path}\n❌ {n_conflicts} events have multiple labels set!"
        else:
            return f"📂 {path}\n✅ All events have exactly one label."

    except KeyError as e:
        return f"📂 {path}\n⚠️  Missing field: {e}"
    except Exception as e:
        return f"📂 {path}\n💥 Unexpected error: {e}"


# Run in parallel
if __name__ == "__main__":
    print("🔄 Checking files in parallel...\n")

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(check_file, path) for path in paths]
        for future in as_completed(futures):
            print(future.result())

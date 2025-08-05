# EYCT Setup Guide

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/Apranikstar/EYCT.git
cd EYCT
```

### Step 1: Configure the Scenario

Open the configuration file and choose one of the following scenarios by setting the appropriate number:

- `1` → $W(e\nu)W^*(jj)$  
- `2` → $W(jj)W^*(e\nu)$  
- `3` → $W(\mu\nu)W^*(jj)$  
- `4` → $W(jj)W^*(\mu\nu)$

### Step 2: Set Output Directory and CPU Count

Edit the `run_all.sh` script to set your desired output directory and number of CPUs:

```ini
OUTDIR="./output/"
NCPUS=8
```

### Step 3: Run the Script

Make the script executable and run it:

```bash
chmod +x run_all.sh
./run_all.sh
```

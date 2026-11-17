import os
import sys
import time
import json
import io
import contextlib
import tempfile
import base64

os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()
RR_DIR = r'c:\Users\Asus-2025\Downloads\RR'
os.chdir(RR_DIR)

nb_path = os.path.join(RR_DIR, 'RR_SupeRR_Selector_Complete_Cricket_EDA_and_Pressure_Analysis.ipynb')
print(f"Reading master notebook: {nb_path}")

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

exec_globals = {
    '__name__': '__main__',
    '__file__': nb_path,
}

# Ensure matplotlib is in Agg mode to avoid any UI block
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

execution_counter = 1
total_code_cells = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
print(f"Total code cells to execute: {total_code_cells}")

start_total_time = time.time()

for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source_code = ''.join(cell['source'])
        first_line = source_code.splitlines()[0] if source_code.splitlines() else "Code cell"
        print(f"\n[{execution_counter}/{total_code_cells}] Running Cell {idx + 1}: {first_line[:75]}")
        
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        captured_displays = []

        def custom_display(*args, **kwargs):
            for arg in args:
                if hasattr(arg, 'data') and hasattr(arg, 'format'):
                    data_b64 = base64.b64encode(arg.data).decode('utf-8') if isinstance(arg.data, bytes) else arg.data
                    mime = f"image/{arg.format.lower()}" if arg.format else "image/png"
                    captured_displays.append({
                        "output_type": "display_data",
                        "data": {mime: data_b64},
                        "metadata": {}
                    })
                elif hasattr(arg, '_repr_png_'):
                    png_bytes = arg._repr_png_()
                    data_b64 = base64.b64encode(png_bytes).decode('utf-8') if isinstance(png_bytes, bytes) else png_bytes
                    captured_displays.append({
                        "output_type": "display_data",
                        "data": {"image/png": data_b64},
                        "metadata": {}
                    })
                else:
                    print(str(arg))

        exec_globals['display'] = custom_display

        cell_start = time.time()
        cell_outputs = []

        try:
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(source_code, exec_globals)
        except Exception as e:
            err_msg = f"Error in cell {idx + 1}: {e}"
            print(f"  FAILED: {err_msg}", file=sys.stderr)
            cell_outputs.append({
                "output_type": "error",
                "ename": type(e).__name__,
                "evalue": str(e),
                "traceback": [err_msg]
            })

        cell_duration = time.time() - cell_start

        # Check for open matplotlib figures and capture them
        fig_nums = plt.get_fignums()
        if fig_nums:
            for num in fig_nums:
                fig = plt.figure(num)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                buf.seek(0)
                img_b64 = base64.b64encode(buf.read()).decode('utf-8')
                captured_displays.append({
                    "output_type": "display_data",
                    "data": {"image/png": img_b64},
                    "metadata": {}
                })
            plt.close('all')

        out_text = stdout_buf.getvalue()
        err_text = stderr_buf.getvalue()

        if out_text:
            cell_outputs.append({
                "output_type": "stream",
                "name": "stdout",
                "text": [line + '\n' for line in out_text.rstrip('\n').split('\n')]
            })
            lines = out_text.strip().splitlines()
            print(f"  Outputs: {len(lines)} lines (took {cell_duration:.2f}s)")
            if lines:
                print(f"  Summary: {lines[-1][:90]}")

        if err_text:
            cell_outputs.append({
                "output_type": "stream",
                "name": "stderr",
                "text": [line + '\n' for line in err_text.rstrip('\n').split('\n')]
            })
            print(f"  Stderr: {err_text[:200]}")

        cell_outputs.extend(captured_displays)

        cell['execution_count'] = execution_counter
        cell['outputs'] = cell_outputs
        execution_counter += 1

total_duration = time.time() - start_total_time
print(f"\nAll {total_code_cells} code cells executed in {total_duration:.2f} seconds.")

# Save executed notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print(f"Saved executed notebook to: {nb_path}")

# Also mirror to artifacts
art_dir = r'C:\Users\Asus-2025\.gemini\antigravity\brain\4fe6158e-0e76-450a-898e-f6d09dd602e6'
shutil.copy2(nb_path, os.path.join(art_dir, 'RR_SupeRR_Selector_Complete_Cricket_EDA_and_Pressure_Analysis.ipynb'))
print("Mirrored executed notebook to artifacts.")

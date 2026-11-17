import json
import os
import sys
import io
import contextlib
import base64

nb_path = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\Rajasthan_Royals_Pressure_Analysis.ipynb'
alt_nb_path = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\pressure_analysis.ipynb'

print(f"Reading notebook from: {nb_path}")
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Shared global namespace for execution
exec_globals = {
    '__name__': '__main__',
    '__file__': nb_path,
}

execution_counter = 1

for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source_code = ''.join(cell['source'])
        print(f"\n--- Executing Code Cell {idx + 1} (Execution count: {execution_counter}) ---")
        
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        
        # Display capture hook
        captured_displays = []
        def custom_display(*args, **kwargs):
            for arg in args:
                # Check if it's an IPython Image
                if hasattr(arg, 'data') and hasattr(arg, 'format'):
                    data_b64 = base64.b64encode(arg.data).decode('utf-8') if isinstance(arg.data, bytes) else arg.data
                    mime = f"image/{arg.format.lower()}" if arg.format else "image/png"
                    captured_displays.append({
                        "output_type": "display_data",
                        "data": {
                            mime: data_b64
                        },
                        "metadata": {}
                    })
                elif hasattr(arg, '_repr_png_'):
                    png_bytes = arg._repr_png_()
                    data_b64 = base64.b64encode(png_bytes).decode('utf-8') if isinstance(png_bytes, bytes) else png_bytes
                    captured_displays.append({
                        "output_type": "display_data",
                        "data": {
                            "image/png": data_b64
                        },
                        "metadata": {}
                    })
                else:
                    print(str(arg))

        exec_globals['display'] = custom_display

        cell_outputs = []
        try:
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(source_code, exec_globals)
        except Exception as e:
            err_msg = f"Error executing cell {idx + 1}: {e}"
            print(err_msg, file=sys.stderr)
            cell_outputs.append({
                "output_type": "error",
                "ename": type(e).__name__,
                "evalue": str(e),
                "traceback": [err_msg]
            })

        out_text = stdout_buf.getvalue()
        err_text = stderr_buf.getvalue()

        if out_text:
            cell_outputs.append({
                "output_type": "stream",
                "name": "stdout",
                "text": [line + '\n' for line in out_text.rstrip('\n').split('\n')]
            })
            print(f"Stdout:\n{out_text[:300]}...")

        if err_text:
            cell_outputs.append({
                "output_type": "stream",
                "name": "stderr",
                "text": [line + '\n' for line in err_text.rstrip('\n').split('\n')]
            })
            print(f"Stderr:\n{err_text[:200]}")

        # Add captured display outputs
        cell_outputs.extend(captured_displays)

        cell['execution_count'] = execution_counter
        cell['outputs'] = cell_outputs
        execution_counter += 1

# Save executed notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

with open(alt_nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("\n" + "=" * 60)
print(f"SUCCESS: Executed all code cells in {nb_path}!")
print("=" * 60)

import os
import shutil
import platform
import ctypes


def deploy_studio_tools(server_script_path):
    # 1. Determine the Resolve Scripting path based on OS
    system = platform.system()
    if system == "Windows":
        resolve_path = os.path.expandvars(
            r"%AppData%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Scripts"
        )
    elif system == "Darwin":  # macOS
        resolve_path = (
            "/Library/Application Support/Blackmagic Design/DaVinci Resolve/"
            "Developer/Scripting/Scripts"
        )
    else:
        print("Unsupported Operating System.")
        return

    # 2. Define the 'Try Studio' subfolder
    target_folder = os.path.join(resolve_path, "Try_Studio_Tools")

    # 3. Create Symlink (Best for Studios) or Copy Folder
    # A Symlink ensures that if you change the script on the server,
    # the editor's machine updates automatically.
    try:
        if os.path.exists(target_folder):
            if os.path.islink(target_folder):
                os.unlink(target_folder)
            else:
                shutil.rmtree(target_folder)

        # Create the link (Requires Admin/Developer Mode on Windows)
        if system == "Windows":
            os.symlink(server_script_path, target_folder, target_is_directory=True)
        else:
            os.symlink(server_script_path, target_folder)

        print(f"✅ Successfully deployed Try Studio Tools to: {target_folder}")
        print(
            "Editors can now find the tools under Workspace > Scripts > Try_Studio_Tools"
        )

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        print("Note: On Windows, you may need to run this script as Administrator.")


# --- EXECUTION ---
# Path to your master scripts on the Try Studio server
SERVER_PATH = r"Z:\Production\Pipeline\Resolve_Scripts\Master_Collection"
# deploy_studio_tools(SERVER_PATH)

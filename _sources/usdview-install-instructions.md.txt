# Installing usdview and Setting Up Python

In this module, we'll be conducting hands-on exercises using usdview, a lightweight and free application developed by Pixar Animation Studios. usdview is an essential tool for viewing, navigating, and introspecting OpenUSD scenes, and we'll be using it for several of our Learn OpenUSD modules.

Before we begin, you'll need to set up usdview on your system. usdview is compatible with Linux, macOS, and Windows. These instructions were written for Windows or Linux users. If you're using macOS, you can still run usdview, but you'll have to build it yourself using the [OpenUSD repository](https://github.com/PixarAnimationStudios/OpenUSD).

## Downloading the Libraries and Tools

First, let's download USD and Python.

1. Go to NVIDIA's [OpenUSD developer resources page](https://developer.nvidia.com/usd).
2. Head to the **Getting Started** section.

![](./images/usdview-install-instructions/usdview-image2.png)

3. Download the OpenUSD libraries and tools that are suitable for your operating system.

![](./images/usdview-install-instructions/usdview-image7.png)

4. After downloading zipped folder, **extract all**. This may take a while.

5. Once the folder has finished unzipping, **rename** the extracted folder to `usd_root`

![](./images/usdview-install-instructions/usdview-folder_rename.mp4)

We will be referring to this folder as `usd_root/` going forward.

Now, let’s make sure everything works. We’ll be using Visual Studio Code in Windows for this example, but you can use your preferred IDE instead. 

``````{note}
**For Linux:** The following instructions are required to install missing X11 dependencies for Ubuntu. Do this before proceeding to the next step. We tested on Ubuntu 22.04 LTS and 24.04 LTS. You may need to adjust this command for newer versions of Ubuntu or other Linux distros.

Run:  
```sh
sudo apt-get install libxkbcommon-x11-0 libxcb-xinerama0 libxcb-image0 libxcb-shape0 libxcb-render-util0 libxcb-icccm4 libxcb-keysyms1
```
``````

6. Open Visual Studio Code.  
7. Under **File > Open Folder**, find your `usd_root/` folder.  

![](./images/usdview-install-instructions/usdview-image13.png)

8. Open a new terminal by going to **Terminal > New Terminal.**

![](./images/usdview-install-instructions/usdview-image1.png)

In this example, we are using PowerShell on Windows for our default terminal.

9. In the terminal, type the following command:  

Windows:
```powershell
.\scripts\usdview_gui.bat
```
Linux/macOS:
```sh
./scripts/usdview_gui.sh
```

10. Then, press **Enter**. It will open usdview’s `HelloWorld.usda` file.

Running `.\scripts\usdview_gui.bat` does not require a USD file to run the application. You can also run `.\scripts\usdview.bat`, but it requires you to provide a USD file as an argument.

Now is a good time to familiarize yourself with [how to navigate the within the viewport](https://docs.omniverse.nvidia.com/usd/latest/usdview/viewport.html#navigation).

11. Close usdview and proceed to the next step.

```{note} 
For quick access, you can add the `scripts/` folder in your `PATH` environment variable, but this isn’t required for these modules.
```

(setting-up-python-env)=
## Setting Up the Python Environment

The prebuilt OpenUSD binaries come with a version of Python to ensure a compatible Python environment. It is located under the `python` folder.

![](./images/usdview-install-instructions/usdview-image5.png)

Here we will be going through how to set up a Python virtual environment and installing `usd-core` via `pip.`

We will be creating the virtual environment using Visual Studio Code.

1. Open Visual Studio Code.  
2. Go to **File > Open Folder.**

![](./images/usdview-install-instructions/usdview-image10.png)

3. Open your downloaded OpenUSD binaries folder that you renamed to `usd_root/`.

![](./images/usdview-install-instructions/usdview-image13.png)

4. Open a terminal window by going to **Terminal > New Terminal**.

![](./images/usdview-install-instructions/usdview-image1.png)

5. Run the following command in the terminal:   

Windows:
```powershell
.\python\python.exe -m venv .\python-usd-venv
```
Linux/macOS:
```sh
./python/python -m venv ./python-usd-venv
```

This will create a virtual Python environment in the current root directory. 

![](./images/usdview-install-instructions/usdview-image12.png)

How to use the virtual environment depends on your platform and shell you are using. Please refer to the following table (which can also be found in the [Python documentation](inv:python:std#venv-explanation)), We've adapted the commands from the Python documentation to reflect the virtual environment name that we used in previous steps.

```{include} ./_includes/venv-table.md
```

``````{note}
For Windows/PowerShell, you may need to also set your execution policy first to allow the script to run. You can use the following command:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
``````
6. Activate your virtual environment with the appropriate command from the table above. The screenshot below shows the Windows command in PowerShell, and the proper response showing our Python virtual environment is now in use.

![](./images/usdview-install-instructions/usdview-image15.png)

## Installing usd-core

Now we’ll install usd-core, which is a dependency that enables us to use the USD API. 

1. Make sure to activate and run the Python virtual environment, which we did in the previous step. With the environment activated, run the following command to install `usd-core`.

Windows:
```powershell
pip install usd-core
```
Linux/macOS:
```sh
pip install usd-core
```

![](./images/usdview-install-instructions/usdview-image3.png)

2. To check if `usd-core` has installed properly we can run the following command in your virtual environment.   

Windows:
```powershell
python -c "from pxr import Usd;print(Usd.GetVersion())"
```
Linux/macOS:
```sh
python -c "from pxr import Usd;print(Usd.GetVersion())"
```

![](./images/usdview-install-instructions/usdview-image4.png)

If successful, it will print out the current USD version. 

Now you can use `usd-core` libraries inside your virtual environment. 

## Installing Assimp

1. Make sure to activate and run the Python virtual environment. If you’re continuing from the previous section, this should already be complete.  
2. With the environment running, run the following command to install `assimp`.

Windows:
```powershell
pip install assimp-py==1.0.8
```
Linux/macOS:
```sh
pip install assimp-py==1.0.8
```

```{attention}
Ensure you are installing assimp-py version **1.0.8** and not a newer version.
```

![](./images/usdview-install-instructions/usdview-image6.png)

3. To check if `Assimp` has installed properly we can run the following command in the virtual environment 

Windows:
```powershell
python -c "import assimp_py"
```
Linux/macOS:
```sh
python -c "import assimp_py"
```

![](./images/usdview-install-instructions/usdview-image8.png)

If you received: `ModuleNotFoundError: No module named 'assimp_py'` then Assimp did not install properly. Otherwise, you are good to go.

Congratulations, you have everything you need installed to complete the Learn OpenUSD modules with usdview. 

## Resuming a Module

If you are unable to complete this module in a single session or if you ever want to return to this module to refresh your knowledge, these are the steps you need to take to re-enable your environment.

1. Open Visual Studio Code.  
2. Go to **File > Open Folder.**

![](./images/usdview-install-instructions/usdview-image10.png)

3. Open your `usd_root/` folder.

![](./images/usdview-install-instructions/usdview-image13.png)

4. Open a terminal window by going to **Terminal > New Terminal**.

![](./images/usdview-install-instructions/usdview-image1.png)

5. Run the appropriate command for your platform/shell to enable the virtual environment we previously created:   

```{include} ./_includes/venv-table.md
```

The screenshot below shows the Windows command in PowerShell, and the proper response showing our Python virtual environment is now in use.

![](./images/usdview-install-instructions/usdview-image15.png)
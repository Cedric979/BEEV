Here I will explain how to create the contianer/app on Docker. This will only be required to do one time.
PLEASE READ UNTIL THE END

Before extract files


1 - Download and install Docker: https://www.docker.com/products/docker-desktop (Make sure to install with your corresponding OS)

2 - Create a folder and copy the scripts/python files and images used to run the interface into this folder.
    In this same folder should be a txt with the names of all the required libraries and which version to use.
    This txt file should be named 'requirements' and it should look like this:

numpy==1.21.4
pandas==1.3.5
streamlit==1.2.0
sklearn==0.0
gspread==5.1.1

3 - Create a new file with NO extension and save it on the folder you created in step 2

4 - In this new file, you will include the following lines:



5 - Open the terminal in your computer and go inside your folder.
    You can either open the terminal directly on the folder, or navigate to it inside the terminal.
    When you are at the correct path, run the following command line:

    docker build -t streamlit_beev:latest .

    INCLUDE the dot at the end
    Wait for it to finish running(can take up to some minutes).

    LEAVE THE TERMINAL OPEN!

6 - Open Docker Desktop now, click on the 'Images' on the left side menu.
    If you've done everything right, there should be an image with the name 'streamlit_beev'. Do not click on it.


7 - Go back to the terminal and run the following command line:

    docker run -p 8501:8501 --name beev_replace streamlit_beev:latest



8 - Go to Docker, and this time click on 'Containers/Apps' on the left side menu.
    If you've done everything right, there should be a container/app named 'beev_replace'.

    Hover over this container, and you will see several options on the right side.
    Click 'Open in browser' and this will open the Interface on your browser. 



    Congratulations, it is now ready for use! 
    
    After this, whenever you want to run you need only to:
    - Open Docker Desktop and click on Containers/apps
    - Hover over the correct container and click on 'Start' and then 'Open in Browser'
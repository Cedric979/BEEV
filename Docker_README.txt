Here I will explain how to create the container/app on Docker. This will only be required to do one time.
PLEASE READ UNTIL THE END



1 - Download and install Docker: https://www.docker.com/products/docker-desktop(Make sure to install with your corresponding OS)
    After installation, open Docker


2 - Create a new folder anywhere in your computer.
    Extract the files in the zip that we sent you into this new folder


3 - Open the terminal in your computer and navigate to your folder(inside the terminal)
    You can also just open the terminal at the folder. 
    Regardless, when you are at the correct path, run the following command line:

    docker build -t streamlit_beev:latest .

    INCLUDE the dot at the end
    Wait for it to finish running(can take up to some minutes).

    LEAVE THE TERMINAL OPEN!


4 - Open Docker Desktop now, click on the 'Images' on the left side menu.
    If you've done everything right, there should be an image with the name 'streamlit_beev'. Do not click on it.


5 - Go back to the terminal and run the following command line:

    docker run -p 8501:8501 --name beev_replace streamlit_beev:latest



6 - Go to Docker, and this time click on 'Containers/Apps' on the left side menu.
    If you've done everything right, there should be a container/app named 'beev_replace'.

    Hover over this container, and you will see several options on the right side.
    Click 'Open in browser' and this will open the Interface on your browser. 



    Congratulations, it is now ready for use! 
    
    After this, whenever you want to run you need only to:
    - Open Docker Desktop and click on Containers/apps
    - Hover over the correct container and click on 'Start' and then 'Open in Browser'
### Threading in Python

By default python procedural way doesn't support threading. If a function needs to be run
'n' number of times, There wouldn't be any concurrency. The second function will run only after 
the first one gets completed.

**Example**

```
import time

start = time.perf_counter()

def do_something():
    print("Start to sleep")
    time.sleep(1)
    print("Done Sleeping")

do_something()
do_something()

finish = time.perf_counter()

print("Time took: ", round(finish - start, 2))
```

In the above code, we are creating a timer which calculates the start and end time. We have created a function `do_something`. This function sleeps for a second. Now if we run this function once. It will sleep for a second and finish. The duration would be 1.0 seconds. However if you want to run the same function multiple times, It takes 'n x 1' times. In our example we ran function twice, thus it takes 2.0 seconds

**Output**

```
Start to sleep
Done Sleeping
Start to sleep
Done Sleeping
Time took:  2.0
```

This will be difficult to handle if we have to run the function multiple time. This creates performance lagging/slowness for the code. Now to sort this lets use threading (Built-In python module). 

### Using threading approach

We have to create couple of threads and map the function to those threads. That way we can achieve concurrency.

**Example**

```
import threading
import time

start = time.perf_counter()

def do_something():
    print("Sleeping 1 second...")
    time.sleep(1)
    print("Done Sleeping...")

t1 = threading.Thread(target=do_something)
t2 = threading.Thread(target=do_something)

t1.start()
t2.start()

t1.join()
t2.join()

finish = time.perf_counter()

print("Duration: ", round(finish - start, 2))
```

Above code, we imported python inbuilt module `threading`. now we create couple of thread instances 't1' & 't2' and assign the target function. we have started threads with `t1.start()` & `t2.start()`. We must join the threads inorder to avoid executing code before the threads complete using `t1.join()` $ `t2.join()`


**Output**

```
Sleeping 1 second...
Sleeping 1 second...
Done Sleeping...
Done Sleeping...
Duration: 1.0 
```

If you see this time the Duration for two threads is same 1.0 seconds. Now lets try the same with a for loop. We trying with for loop because real world example would not be with manual 'n' number of thread instances.

### Threads using for loop

```
threads = []

for _ in range(10):
    t = threading.Thread(target=do_something)
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()
```

We just replaced the thread instances with the above code. firstly we created an empty list `threads`. This is to store the thread instances. we use `range(10)` to loop 10 times. we start the threads and append the thread instances to the list we created before. Finally we could loop the threads and join them.

**Output**

```
Sleeping 1 second...
Sleeping 1 second...
...
...
Done Sleeping...
Done Sleeping...
...
...
The Function completed in 1.01 second(s)
```

The result would be surprisingly 1.01 for ten threads too. This is because the functions been created as different threads and started concurrently.

*Note: We could use the arguments with args=[argument_value] in the thread instances. The type of argument should be in list*

`t = threading.thread(target=<function>, args=[<arguments>])`

### Real world Example

Let's build a image downloader with python for the real world threading example. we use https://unsplash.com/ for this example. Unsplash has Over 2 million free high-resolution images by the world’s most generous community of photographers. For this tutorial we are going to use python's `requests` library and `BeautifulSoup`. `BeautifulSoup` to grab the image download URLs and `requests` library to download the image and write it to a file. Initially we are not going to use the thread. Instead we are going to manually run a for loop to download the images.


Firstly we import the required modules. time, requests and bs4

```
import time
import requests
from bs4 import BeautifulSoup
```

Then we create an empty array to store the grabbed image URLS

```
img_url = []
```

Lets create a function to grab the download link url from the webpage URL. we use requests module to send the get request. We use BeautiFulSoup to parse the html and get all the anchor tags with `findAll` method and append them to the list `img_url`

```
def get_urls(URL):
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.content, 'html.parser')
    anchor_tag = soup.findAll("a", {"title" : "Download photo"})

    for i in anchor_tag:
        get_link = i["href"]
        img_url.append(get_link)
```

Now, we got the list of download link urls. Let's make use of it to download the image and save it. The below function will get the content of the URL and save it to the file in 'Images' directory. we must write the file in "wb" mode.

```
def download_images(URL):
    file_name = "Images/"+URL.split('/')[4]+".jpg"
    resp = requests.get(URL)
    
    file = open(file_name, "wb")
    file.write(resp.content)
    file.close()
```

Let's create a `main` function with the timer and run the `get_url` function. Now we can loop through the list and download the images 

```
def main():
    start = time.perf_counter() 
    print(f"Grabbing the URLs...")
    get_urls('https://unsplash.com/t/nature')
    print("Downloading the Images")

    for link in img_url:
        download_images(link)
    
    finish = time.perf_counter()
    print(f"{len(img_url)} Images Downloaded in {round(finish - start, 2)} second(s)")

if __name__ == '__main__':
    main()
```

**Output**

```
Grabbing the URLs...
Downloading the Images
20 Images Downloaded in 27.88 second(s)
```

As we see in output, 20 images took 27.88 seconds to download since we didn't use any threads.
Now lets alter the code a bit to improve the speed.

```
def main():
    start = time.perf_counter() 
    print(f"Grabbing the URLs...")
    get_urls('https://unsplash.com/t/nature')
    print("Downloading the Images")

    threads = []

    for link in img_url:
        t = threading.Thread(target=download_images, args=[link])
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    
    finish = time.perf_counter()
    print(f"{len(img_url)} Images Downloaded in {round(finish - start, 2)} second(s)")
```

In `main` section, we created an empty list to store the threads. Then we created threads looping our `img_url` list. We create another loop to join the threads. This avoids the thread execution to move further without downloading all the images.

Now the result would be surprising.

**Output**

```
Grabbing the URLs...
Downloading the Images
20 Images Downloaded in 8.34 second(s)
```
As you can see the output, Threads reduced the time from `27.88 second(s)` to `8.34 second(s)`

### ThreadPoolExecutor

We can also use ThreadPoolExecutor for the same. This would be simplified than using the threads. we don't need threading module. we are going to use `ThreadPoolExecutor` from `concurrent.futures` module.

We're going to import the module first

```
import concurrent.futures
```

Then we need to alter the code like below

```
with concurrent.futures.ThreadPoolExecutor() as executor:
        for link in img_url:
            executor.submit(download_images, link)
```

We removed all the threading from the main function and replaced the above code. We are using ThreadPoolExecutor and looping the `img_url`. Then we submit the executor with the function `download_images` and passing the link as an attribute. This would do the same thing, which we did with threading.

The Output seems similar.

```
Grabbing the URLs...
Downloading the Images
20 Images Downloaded in 7.92 second(s)
```


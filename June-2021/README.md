# June 2021 Take Home!

## What it is...

1. Download the data folder onto your local computer.

2. Create a python script that:

   1. Reads a random selects a random "n" number which is bound between 0 and "M" where M is the number of files inside of the data folder.
   2. Given a number "n" select a subset of the files in the folder such that "n" files are selected.
   3. Grab all the data inside of the files and "union" it together into a JSON object.

3. Create Docker container that:

   1. Is a Flask api (try to use Flask 2.0 since it's recently released)
   2. The Flask app exposes a port to your local computer that accepts "post" requests from STEP 2 of this take home (i.e. the JSON)
   3. The Flask Dockerfile should use docker.io/abelbarrera15/spark (https://hub.docker.com/r/abelbarrera15/spark) as a base image. You can read about base images here: https://docs.docker.com/develop/develop-images/baseimages/
   4. By using the base image above, that means your container will have spark installed on it. You can "invoke" spark by using "CMD" instead of "RUN" (under #Run Tests) as in this repo: https://github.com/ksmc/RL-cleanse-standardize-app/blob/master/Dockerfile.
   5. Given the JSON payload, your code should print into the terminal two things:
   6. The top 10 words in the payload (consider standardizing the word such as case sensitivity, the use of "." at the end of sentences, etc. etc.)
   7. The cities that had the most rows associated (in that order) to it and the top ten words associated to the city in for example this format:
      [
      {'Hyderabad' : [{'SomeWord':10},{'SomeWord2'}:08}]},
      {'Pune' : [{'SomeWord':5},{'SomeWord2'}:4}]},
      {'Chennai' : [{'SomeWord':2},{'SomeWord2'}:1}]},
      ]
   8. The code you use MUST be using PySpark for this portion. Map Reduce might be a good approach for this! RDD or DataFrames are OK.
   9. Set up this code so you can run it using "docker-compose" and the application should run forever so long as the docker-compose is "up"

4. In summary, the python script in #2 will send a POST request to the Flask API from #3 and #3 will print on the terminal that the docker-compose was ran on the most popular words and most popular cities on rows as well as the popular words associated to those.

## Must Dos...

1. Use DocStrings
2. Save a requirement.txt file
3. Consider code complexity (i.e. O(n) complexity https://dzone.com/articles/learning-big-o-notation-with-on-complexity#:~:text=O(n)%20represents%20the%20complexity,after%20reading%20all%20n%20elements)
4. The docker component should be written AS MUCH as possible in PySpark using Distributed Computing concepts.

## Don't forget -- send us your solution by the FIRST Wednesday of June (7th). We will then upload it to this repo so all people can see what people tried to solve the problem.

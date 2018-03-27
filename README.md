# Information Extraction

Source code of the post: http://philipperemy.github.io/information-extract/

Understanding articles, reports and generate a graph based (unsupervised learning).


<p align="center">
  <img src="static/img_1.png">
</p>

## Get Started (Linux/Mac OS)

```
git clone --recursive https://github.com/reactiveai/information-extraction.git

# run this if you forgot to add --recursive flag when git cloning.
# git submodule update --init --recursive
# git submodule foreach git pull origin master

chmod +x init.sh
./init.sh

python server.py
```

From:

```
Google is expanding its pool of machine learning talent with the purchase of a startup that specializes in 'instant' smartphone image recognition.

On Wednesday, French firm Moodstocks announced on its website that it's being acquired by Google, stating that it expects the deal to be completed in the next few weeks. There's no word yet on how much Google is paying for the company.

Moodstocks' "on-device image recognition" software for smartphones will be phased out as it joins Google. Moodstocks' team will also move over to Google's R&D center in Paris, according to Google's French blog. 

"Ever since we started Moodstocks, our dream has been to give eyes to machines by turning cameras into smart sensors able to make sense of their surroundings," Moodstocks said in a statement on its site. "Our focus will be to build great image recognition tools within Google, but rest assured that current paying Moodstocks customers will be able to use it until the end of their subscription."
```

To (without dominating decision rules):

<p align="center">
  <img src="http://philipperemy.github.io/information-extract/hello2.png">
</p>

And (with dominating decision rules):

<p align="center">
  <img src="http://philipperemy.github.io/information-extract/hello.png">
</p>




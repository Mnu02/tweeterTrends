# tweeterTrends

In this project, I developed a geographic visualization of Tweeter data across the United States of America using lists, dictionaries, and data abstraction techniques to create a modular program.

At the end, the program will be able to draw how different states feel about Texas and this is going to be through:
- Collecting public Twitter posts (tweets) that have been tagged with geographic locations and filtering for those that contain the "texas" query term
- Assigning a sentiment (positive or negative) to each tweet, based on all of the words it contains
- Aggregating tweets by the state with the closest geographic center, and finally
- Coloring each state according to the aggregate sentiment of its tweets. ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `#f03c15` means positive sentiment; ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) `#1589F0` means negative

## Usage
I am going to querry the following commands. Remember that ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `#f03c15` == positive sentiment and ![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) `#1589F0` == negative sentiment

### To know how people feel about Texas
`python3 trends.py -m texas`
<img width="969" alt="Screen Shot 2023-07-09 at 17 19 10" src="https://github.com/Mnu02/tweeterTrends/assets/115519540/6bcde185-92ff-44e8-a03b-5ae0a1ad47dd">

### To know how people feel about Sandwiches
`python3 trends.py -m sandwiches`
<img width="971" alt="Screen Shot 2023-07-09 at 17 21 40" src="https://github.com/Mnu02/tweeterTrends/assets/115519540/5dc4d66b-40d6-41df-98ee-a29b42416d22">


### To know how people feel about the Former President Obama
`python3 trends.py -m obama`
<img width="973" alt="Screen Shot 2023-07-09 at 17 20 37" src="https://github.com/Mnu02/tweeterTrends/assets/115519540/7f13058e-8f65-4a53-a66f-d6f559bbf295">


## Acknowledgements
Aditi Muralidharan developed this project with John DeNero. Hamilton Nguyen extended it. Keegan Mann developed the autograder. Many others have contributed as well.

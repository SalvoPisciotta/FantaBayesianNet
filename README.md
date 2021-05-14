# :mage: FantaBayesianNet :soccer:

This repository contains a project realized as part of the *Fundamentals of Artificial Intelligence* exam of the [Master's degree in Artificial Intelligence, University of Bologna](https://corsi.unibo.it/2cycle/artificial-intelligence), specifically in the module about uncertainty and probabilistic reasoning, held by professor Paolo Torroni.

In this work, we used a *Bayesian Network* to model relevant factors of player performance in the presence of noisy data. We apply our analysis to the 2020–2021 season in the top Italian league, Serie A, and use the player ratings provided by a popular Italian fantasy football game, the so-called **Fantacalcio**.

The **goal** is to explore the causal relations that allow to predict if a football player can be deployed or not in a fantasy football lineup. Different kind of reasoning are done to exploit the flow of influence between variables and possible independences. 



## Dataset

Since statistics of single football players of Serie A in each mach are not directly accessible and they are distributed on different web sites, we have developed a [web scraping script](https://github.com/giuseppeboezio/FantaBayesianNet/blob/main/src/preprocessing.py) able to collect data from [Fantacalcio.it](https://www.fantacalcio.it/statistiche-serie-a) and [Transfermarket.it](https://www.transfermarkt.it/serie-a/startseite/wettbewerb/IT1).

We decided to select only forwards, since their statistics are the most interesting from the view point of the Fantacalcio, and we picked an average of 2 players per team for a total of 40 players.

These data inside this [folder](data) are about the first 30 rounds of the 2020–2021 Serie A season.



## Results

The results provided in the [notebook](https://github.com/giuseppeboezio/FantaBayesianNet/blob/main/src/FantaBayesianNet.ipynb) are reasonable admissible but since we tried to make inference about a complete stochastic domain, it found out to be really difficult to obtain good results because it was not always possible to take into account the enormous amount of variables that effectively affect the domain of our analysis and construct a model on it. A possible different analysis based on our model could be to extend the dataset of players, considering not only forwards but also midfielders and defenders in order to prove whether the model could be a good base to develop a real software that helps fantasy managers to solve their doubts in line up their fantasy football formation.



## Resources & Libraries

* [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)
* [pgmpy](https://github.com/pgmpy/pgmpy)


## Versioning

We use Git for versioning.



## Group members

|  Reg No.  |  Name     |  Surname  |     Email                              |    Username      |
| :-------: | :-------: | :-------: | :------------------------------------: | :--------------: |
|   997317  | Giuseppe  | Murro     | `giuseppe.murro@studio.unibo.it`       | [_gmurro_](https://github.com/gmurro)         |
|   985203  | Salvatore | Pisciotta | `salvatore.pisciotta2@studio.unibo.it` | [_SalvoPisciotta_](https://github.com/SalvoPisciotta) |
|  1005271  | Giuseppe  | Boezio    | `giuseppe.boezio@studio.unibo.it`      | [_giuseppeboezio_](https://github.com/giuseppeboezio) |


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
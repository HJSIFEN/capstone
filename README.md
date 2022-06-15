# 빅데이터를 이용한 SEO분석

<br>

## Description
 블로그 크롤링을 통해 상위 블로그의 특징을 알아내고 유저의 블로그와 비교한다.<br>
<br>

>input: 유저의 블로그 URL<br>
>output: 유저 블로그와 상위 블로그의 비교점(사진, 텍스트)
<br>


## Image Result
<br>

![image](https://user-images.githubusercontent.com/60573146/173763107-4d574a50-af64-499c-8bde-1d4224da205c.png)

<br>


## Code explannation

- 블로그 크롤링<br>

  * __get_data(keywords, client_id, client_secret, naver_api, length)__: api 사용여부 및 전처리 함수
      ```
      keywords: 검색할 키워드
      client_id: (네이버 api 사용시) id코드
      client_secret: (네이버 api 사용시) secret코드
      naver_api: 네이버 api 사용 여부(True, False)
      length: 최대로 검색되는 블로그 개수(최대 1000개)
      ```

  * __blog_search(keyword, length)__: BeautifulSoup를 이용한 크롤링
      ```
      keyword: 검색할 키워드
      length: 최대로 검색되는 블로그 개수(최대 1000개)
      ```

  * __naver_api_blog_url(keyword, client_id, client_secret, length)__: 네이버 api를 이용한 크롤링
      ```
      keywords: 검색할 키워드
      client_id: 네이버 개발자 센터에서 발급되는 id코드
      client_secret: 네이버 개발자 센터에서 발급되는 secret코드
      length: 최대로 검색되는 블로그 개수(최대 1000개)
      ```   
   
   
  * __utils.py__: feature들을 뽑아내는 함수
      ```
      # feature
      text_amount: 본문 분량
      keyword_mentioned: 키워드 언급 횟수
      commentNum: 댓글 개수
      keyword_100: 첫 100단어안에 키워드 포함 여부(포함1, 미포함0)
      keyword_title_data: 제목에 키워드 포함 여부
      link_num_data: 링크 개수
      player_num_data: 동영상 개수
      img_num_data: 이미지 개수
      poDate: 포스트 날짜
      past_date: 현재날짜-포스트 날짜=지난 날짜
      five_day_visitor: 최근 5일동안의 방문자 수 
      ```   
> input: keyword, length 등<br>
> output: 크롤링한 블로그 본문에서 뽑은 feature들의 list
<br>

- Decision Tree<br>

  [Decision Tree 참고 링크](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)<br>
  [export_text 참고 링크](https://scikit-learn.org/stable/modules/generated/sklearn.tree.export_text.html)<br>

  > input: 최적의 decision tree<br>
  > output: 상위 블로그와 비교<br>

    ```
    ex)
    treetext = export_text(dtc, feature_names=data_txt)
    …
    
    상위블로그 조건
    past_date <= 61.50
    text_amount >  839.50
    past_date <= 10.50
    ```


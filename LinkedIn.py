table name: article_views

date  viewer_id  article_id  author_id
2017-08-01  123  456 789
2017-08-02  432  543 654
2017-08-01  789  456 789
2017-08-03  567  780 432.

How many article authors have never viewed their own article?

How many members viewed more than one article on 2017-08-01?


# Not view their own;
select count(distinct author_id)
from article_views
where viewer_id not in
(select viewer_id from article_views where viewer_id = author_id)
;

self_view = article_views[article_views.viewer_id == article_views.author_id][["viewer_id"]].drop_duplicates("viewer_id")
not_self_view = article_views.merge(self_view, left_on = "viewer_id", right_on = "viewer_id", how = "left", indicator = True)
print(not_self_view[not_self_view["_merge"]=="left_only"].drop_duplicates("author_id").shape[0])

# viewed more than 1 article;
select count(distinct viewer_id)
from
(select viewer_id, article_id
from article_views
where date  = "2017-08-01"
group by viewer_id)
having count(distinct article_id) > 1);

# GET RECORDS ON 2017-08-01
article_0801 = article_view[article_view.date == "2017-08-01"]
# Get distinct view/ article combination
df_unq = article_0801.groupby("viewer_id")["article_id"].nunique().to_frame()
df_unq[df_unq.article_id > 1].shape[0]
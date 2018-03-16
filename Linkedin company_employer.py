Table employer:
member_id, company_name, year_start

(1) count members who ever moved from Microsoft to Google?
(2) count members who directly moved from Microsoft to Google? (Microsoft -- Linkedin -- Google doesn't count)

select count(distinct ms.member_id) as count_move
from (select member_id, min(year_start) as ms_year_start from employer where company_name = "Microsoft" group by member_id) ms
left join
(select member_id, company_name, max(year_start) as gg_year_start from employer where company_name = "Google" group by member_id) gg
on ms.member_id = gg.member_id and ms.ms_year_start <= gg.gg_year_start

# python
min_ms = employer[employer.company_name == "Microsoft"].groupby("member_id")["year_start"].min().to_frame().rename(columns = {"year_start": "ms_year"})
max_gg = employer[employer.company_name == "Google"].groupby("member_id")["year_start"].max().to_frame().rename(columns = {"year_start": "gg_year"})
match = min_ms.merge(max_gg, left_index = on, right_index = on, how = "inner")
match[match.ms_year <= match.gg_year].shape[0]


select count(distinct pre.member_id)
from
(select *, row_number() over (partition by member_id order by year_start) as rn
from employer) post
left join
(select *, row_number() over (partition by member_id order by year_start) as rn
from employer) pre
on pre.member_id = post.member_id and post.rn = pre.rn +  1
where pre.company_name =  "Microsoft" and post.company_name = "Google" and post.rn > 1
;

# Python
#employer["Rank"] = employer.groupby("member_id")["year_start"].transform(lambda x: x.rank())
employer["Rank"] = employer.sort_values(by = ["member_id","year_start","company_name"]).\
                            gropuby("member_id").cumcount() + 1
pre_record["Rank"] = employer["Rank"] - 1
match = pre_record["Rank" >= 0].merge(employer, left_on = ["member_id","rank"], right_on = ["member_id","rank"], how = "left")
match[(match.company_name_x == "Microsoft") & (match.company_name_y == "Linkedin")].groupby("member_id").nunique().shape[0]

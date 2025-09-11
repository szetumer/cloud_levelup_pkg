## Level 6: Cleaning Up Resources

IMHO, Azure doesn't do a very good job helping you keep costs __extremely__ low. They're more of a B2B operation than a B2C operation, which makes training difficult because you could spend an extra $20 without realizing it. That's not a big deal for a company, but if you're doing this on your own dime and with your own time, that can sting and keep motivation low.

NOTE: These exercises will help you minimize costs incurred with databricks. If you don't have a databricks workspace up, consider working through levels 4 and 5.

NOTE: Throughout this level, you may get a warning that your query has failed due to throttling. This is because you are placing too much demand on the public API, and they are refusing to run your query. If that is the case, simply skip the queries that are causing your requests to be throttled by deleting those test numbers from the `tests_to_run` parameter in `rgraph_queries.json` file in the Cloud Levelup project.
# GITHUB SEARCH DORKS



[*GitHub Actions*](https://docs.github.com/en/actions) can be a goldmine for finding sensitive information using specific dorks.  
Here is one of many examples of a query that we can input directly into GitHub Search to find potential sensitive information related to AWS accounts by inspecting the action's logs:  

```console
"aws lambda" AND (path:.github/workflows) AND ("publish-version" OR "update-function-configuration" OR "update-function-code")
```    

For a deep dive, read [*this*](https://orca.security/resources/blog/leakycli-aws-google-cloud-command-line-tools-can-expose-sensitive-credentials-build-logs/) article from Orca Security's blog.  



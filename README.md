# read-text-2-llm

create a file `.local_settings` with the following content:

```
export OPENAI_API_KEY="{replace with your own OpenAPI token}}"
```

Then run:
```lang=bash
chmod +x set_me_up.sh
set_me_up.sh
python main.py
```

*** CAVEAT: *** Do not share your API token with anybody. Do not share your running application with anybody you don't trust.
One having your token or using your app means that they can query OpenAPI using your own identity.
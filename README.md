# datastore-backup
Load a backup of Google Datastore into your local `dev_appserver.py`

# Steps

1. Create the backup
2. Download the backup
3. Re-hydrate the backup data into `ndb.Model` entities

# Detailed Steps
1. Create a backup of datastore in a Google Cloud Storage bucket using one of
the following methods. (~5 minutes + backup time)
   1. [Instructions for creating backup](https://cloud.google.com/appengine/docs/standard/python/console/datastore-backing-up-restoring)
   2. [Instructions for creating periodic backup (Alpha)](https://cloud.google.com/appengine/articles/scheduled_backups)

2. Download the backup from the Google Cloud Storage bucket created in the above step.
   1. Install and setup the Google Cloud Tools. The easiest
      way to do so is to download the bucket using `gsutil` ([available here](https://cloud.google.com/sdk/docs/)
      as the latest Google Cloud SDK).
   2. Switch to the project that contains the backups.
      ```bash
      # List out all the projects you have
      > gcloud projects list

      # switch active configuration to example-project-name
      > gcloud config set project example-project
      ```
   3. Download the actual bucket using the name of the bucket that you specified
      in step 1.
      ```bash
      # This will download the specified bucket `.ds_backup` by default
      > ./dsbackup.py <bucket_name>
      ```

3. Use the same `APPLICATION_ID` on your `dev_appserver` or `webtest` that you
   use on your production server. This can be done by setting the
   [APPLICATION_ID on your testbed test](https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.testbed) or setting the `APPLICATION_ID` as an environment variable in your
   `dev_appserver`. Note that your `APPLICATION_ID` in production seems to be
   `"s~" + <project_id>`. So this project name would be `s~example-project`.

4. Hydrate the backup into Datastore entities in test or within
   `dev_appserver` using the following guiding example.

   ```python
   from google.appengine.api.files import records
   from google.appengine.datastore import entity_pb
   from google.appengine.ext import ndb
   import dsbackup

   # Be sure to import all the ndb.Models that your project needs to hydrate!
   # This project only has `User` `ndb.Model`'s so the following is needed:
   from user import User # user.py not included (only example)

   def hydrate():
       for f in dsbackup.get_files():
           raw = open(f, 'r')
           reader = records.RecordsReader(raw)
           for record in reader:
               entity_proto = entity_pb.EntityProto(contents=record)
               entity = ndb.Model._from_pb(entity_proto)
               entity.put()
   ```

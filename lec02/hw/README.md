# Homework Task

Create 2 jobs to process sales from the sales API:

* **Job 1:** take sales from the API and write to the local disk in the JSON format
* **Job 2:** write received sales in the avro format to the stage directory

To run the jobs and checks you need to specify the next environmental variables:

* API_AUTH_TOKEN - the token used to connect to the sales API
* BASE_DIR - the path to the working directory
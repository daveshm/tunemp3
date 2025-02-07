const fileParser = require('express-multipart-file-parser')
const bodyParser = require('body-parser');
const cors = require('cors');
const { Readable } = require('stream');
const { Storage } = require('@google-cloud/storage');
const admin = require("firebase-admin");
admin.initializeApp();

const functions = require('firebase-functions');

const express = require('express');
const app = express();



app.use(fileParser);
app.use(cors({ origin: true }));
app.use(bodyParser.urlencoded({ extended: true }));



app.post('/api/upload/', (req, res) => {
    const gcs = new Storage({
        projectId: 'inference-front-end',
      });
      
    const storage = gcs.bucket("svc_artifacts_fire");

    const file = req.files[0];
    console.log(file); // you can see the file fields here, lots of good info from the parser

    // convert the file buffer to a filestream
    const fileStream = Readable.from(file.buffer);
    
    // upload to firebase storage
    const fileUpload = storage.file(file.originalname);

    // create writestream with the contentType of the incoming file
    const writeStream = fileUpload.createWriteStream({
        metadata: {
            contentType: file.mimetype
        }
    });
    
    // pipe the filestream to be written to storage
    fileStream.pipe(writeStream) 
      .on('error', (error) => {
        console.error('Error:', error);
        res.status(500).send({ message: error });
      })
      .on('finish', () => {
          console.log('File upload complete');
          res.status(200).send({ message: 'File uploaded successfully.'});
      });
});

exports.api = functions.https.onRequest(app);
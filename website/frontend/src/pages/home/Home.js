import React from "react";

import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Spinner,
} from "react-bootstrap";
import axios from "axios";
import { API_URL } from "../../config.js";
import { StlViewer } from "react-stl-viewer";

const Home = () => {
  const [loading, setLoading] = React.useState(false);
  const [result, setResult] = React.useState(false);
  const [preview, setPreview] = React.useState(true);
  const [resultData, setResultData] = React.useState([]);
  const [image, setImage] = React.useState("");
  const [showImage, setShowImage] = React.useState(false);

  const onChangeFile = (e) => {
    setImage(e.target.files[0]);
  };

  const onSubmit = (e) => {
    e.preventDefault();
    if (image === "") {
      alert("Please select a image");
      return;
    }
    setLoading(true);
    setShowImage(true);
    const uploadData = new FormData();
    uploadData.append("image", image);

    console.log(API_URL + "upload");

    axios
      .post(API_URL + "upload", uploadData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => {
        console.log(res);
        setLoading(false);
        if (res.data.status === 200) {
          console.log(res.data);
          setResult(true);
          setResultData(res.data.data);
          setLoading(false);
        } else {
          alert("Something went wrong");
        }
      })
      .catch((err) => {
        console.log(err);
        setLoading(false);
        alert("Something went wrong");
      });
    //setLoading(false);
    //setResult(true);
  };

  const reset = () => {
    setPreview(true);
    setLoading(false);
    setResult(false);
    setImage("");
    setShowImage(false);
    setResultData([]);
  };

  return (
    <Container>
      <Row className="justify-content-center">
        <Col className="h-100" xs={12} md={12} lg={10}>
          <div className="p-2">
            <h3 className="text-center mb-3">Satellite Image to DEM</h3>
            <Card className="shadow rounded-3 p-2">
              <Card.Body>
                {!preview ? (
                  <div>
                    <h5 className="text-center">3D view</h5>
                    <div className="d-flex">
                      <div className="m-auto">
                        <StlViewer
                          style={{
                            top: 0,
                            left: 0,
                            width: "50vw",
                            height: "25vw",
                          }}
                          orbitControls
                          shadows
                          showAxes
                          modelProps={{
                            scale: 0.5,
                            color: "grey",
                          }}
                          url={`http://127.0.0.1:5000/api/model/download/${resultData["id"]}.stl`}
                        />
                      </div>
                      <div>
                        <div>
                          <img
                            src={URL.createObjectURL(image)}
                            alt="input image"
                            className="img-fluid"
                          ></img>
                        </div>
                        <div>
                          <img
                            src={`http://127.0.0.1:5000/api/pdem/download/${resultData["id"]}.png`}
                            alt="output image"
                            className="img-fluid"
                          ></img>
                        </div>
                      </div>
                    </div>
                    <div className="text-center">
                      <Button onClick={reset}>Upload</Button>
                    </div>
                  </div>
                ) : (
                  <React.Fragment>
                    {loading ? (
                      <div className="text-center p-2">
                        <Spinner animation="border" role="status">
                          <span className="visually-hidden">Loading...</span>
                        </Spinner>
                      </div>
                    ) : (
                      ""
                    )}
                    <div className="d-flex">
                      {showImage && (
                        <div
                          className="text-center p-2 m-auto"
                          style={{ flexBasis: "30%" }}
                        >
                          <img
                            src={URL.createObjectURL(image)}
                            alt="input image"
                            className="img-fluid"
                          ></img>
                        </div>
                      )}

                      {result && (
                        <div
                          className="text-center p-2 m-auto"
                          style={{ flexBasis: "30%" }}
                        >
                          <img
                            src={`http://127.0.0.1:5000/api/pdem/download/${resultData["id"]}.png`}
                            alt="output image"
                            className="img-fluid"
                          ></img>
                        </div>
                      )}
                    </div>
                    <Form onSubmit={onSubmit}>
                      <Form.Group
                        className="text-center mb-3"
                        controlId="formBasicEmail"
                      >
                        <Form.Label className="h5">Upload image</Form.Label>
                        <Form.Control
                          type="file"
                          accept="image/*"
                          onChange={onChangeFile}
                        />
                      </Form.Group>
                      <div className="text-center">
                        <Button
                          className="me-3"
                          variant="primary"
                          type="submit"
                          size="md"
                          disabled={loading}
                        >
                          Upload
                        </Button>
                        {result && (
                          <Button
                            className="me-3"
                            variant="primary"
                            size="md"
                            disabled={loading}
                            onClick={() => setPreview(false)}
                          >
                            Show Result
                          </Button>
                        )}
                      </div>
                    </Form>
                  </React.Fragment>
                )}
              </Card.Body>
            </Card>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;

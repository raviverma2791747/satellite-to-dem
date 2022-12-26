import React from "react";
import { Container, Row, Col } from "react-bootstrap";

const Footer = () => {
  return (
    <footer>
      <Container>
        <Row>
          <Col className="text-center">
            <p>Made  by <a href="https://github.com/raviverma2791747">Ravi</a></p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;

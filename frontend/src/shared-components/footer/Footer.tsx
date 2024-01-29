import React from "react";
import { Container, Subtitle, Title, Img } from "./styles";

const Footer = () => (
  <Container>
    <Img src={require("../../assets/imgs/Logo_BHZ.png")} alt="Logo BHZ"/>
    <Title>
      {"Sistema de "}
      <Subtitle>gestão escolar</Subtitle>
    </Title>
  </Container>
);

export default Footer;

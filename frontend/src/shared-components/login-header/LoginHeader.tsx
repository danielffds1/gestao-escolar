import React from "react";
import { Container, Subtitle, Title } from "./styles";
import { Box, Button } from "@mui/material";

const LoginHeader = () => {
  return (
    <Container>
       <img src={require("../../assets/imgs/Logo_BHZ1.png")} alt="Logo BHZ" style={{ width: "150px", height: "89px" }} />
      <Box>
        <Title>Sistema de</Title>
        <Subtitle>gestão escolar</Subtitle>
      </Box>
    </Container>
  );
};

export default LoginHeader;

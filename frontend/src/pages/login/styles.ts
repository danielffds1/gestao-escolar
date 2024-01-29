import { Box, Button, Typography } from '@mui/material'
import { styled } from '@mui/material/styles';

export const Container = styled(Box)(({ theme }) => ({
  width: '100%',
  height: '100%',
  background: theme.palette.primary.main,
  margin: '-8px'
}))

export const Body = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  gap: '24px',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '32px 16px',
}))

export const LoginButton = styled(Button)(({theme}) => ({
  marginTop: '24px'
}))

export const LinkRegister = styled(Typography)(({ theme }) => ({
  fontSize: '15px',
  color: '#707070',
  fontFamily: 'Arial, sans-serif',
  textDecoration: 'none',

  '& a': {
    color: '#0F77D7',
    textDecoration: 'inherit',
  },
}));
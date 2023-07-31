import React from 'react';
import styled from "styled-components";

const AddNewBookPage = styled.div`
    align-content: center;
`;

const AddNewBookBlock = styled.div`
  margin: 10%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
`;

const AddNewBookImgBox = styled.div`
  //width: 200px;
  //height: auto;
`;
// const AddNewBookImg = styled.img`
//
// `;

const AddNewBookInfo = styled.div`
    
`;

const AddNewBook = () => {
    return (
        <AddNewBookPage>
            <h1>Поделиться новой книгой</h1>
            <AddNewBookBlock>
                <AddNewBookImgBox>

                </AddNewBookImgBox>
                <AddNewBookInfo>
                    add new book
                </AddNewBookInfo>
            </AddNewBookBlock>
        </AddNewBookPage>
    );
};

export default AddNewBook;
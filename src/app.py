import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import analyze_credit_card


def configure_interface():
    st.title("Upload de Arquivo Desafio DIO - Documentos falsos")
    uploaded_file = st.file_uploader(
        "Escolha o arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        filename = uploaded_file.name

        # Enviar para o blob do Azure
        blob_url = upload_blob(uploaded_file, filename)

        if blob_url:
            st.write("Enviado com sucesso ao Azure Blob Storage.")
            credit_card_info = analyze_credit_card(blob_url)
            show_image_and_validation(blob_url, credit_card_info)
        else:
            st.write("Erro ao enviar o arquivo para o Azure")


def show_image_and_validation(blob_url, credit_card_info):
    st.image(blob_url, caption="Imagem enviada", use_container_width=True)
    st.write("Resultado da avaliação")

    if credit_card_info and credit_card_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'>Cartão válido<h1>",
                    unsafe_allow_html=True)
        st.write(f"Nome do Titular: {credit_card_info["card_name"]}")
        st.write(f"Banco emissor: {credit_card_info["bank_name"]}")
        st.write(f"Data de validade: {credit_card_info["expiry_date"]}")

    else:
        st.markdown(f"<h1 style='color: red;'>Cartão inválido<h1>",
                    unsafe_allow_html=True)
        st.write(f"Não é um cartão válido.")


if __name__ == "__main__":
    configure_interface()

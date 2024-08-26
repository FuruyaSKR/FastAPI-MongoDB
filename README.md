## Projeto: Sistema de Gerenciamento de Loja de Chapéus

### Visão Geral do Projeto

Este projeto foi desenvolvido para atender às necessidades específicas de uma loja de chapéus, oferecendo uma solução tecnológica que facilita o gerenciamento de coleções de chapéus e as operações de vendas. A aplicação foi construída utilizando **FastAPI**, um framework moderno e eficiente para a criação de APIs em Python, em conjunto com **MongoDB**, um banco de dados NoSQL conhecido por sua flexibilidade e escalabilidade. O objetivo principal deste projeto é automatizar e otimizar as operações da loja, permitindo um gerenciamento eficiente dos produtos e proporcionando uma interface intuitiva para os operadores.

### Motivação e Objetivos

A loja de chapéus enfrentava dificuldades na organização e controle de suas coleções. À medida que a loja crescia e diversificava suas coleções, o gerenciamento manual dos produtos se tornava cada vez mais complexo. A necessidade de uma solução digital robusta e eficiente tornou-se evidente, e este projeto foi desenvolvido para enfrentar esses desafios de forma direta.

Os principais objetivos do projeto incluem:

- **Gerenciamento Eficiente de Coleções**: Capacitar os operadores da loja a criar, atualizar e remover coleções de chapéus de maneira simples e eficaz.
- **Segurança e Auditoria**: Integrar mecanismos de segurança para proteger os dados da loja e implementar auditorias para monitorar operações críticas, garantindo a responsabilidade e transparência.
- **Interface Intuitiva**: Desenvolver uma API RESTful que possa ser facilmente integrada com interfaces de usuário ou outras aplicações de terceiros.

### Estrutura do Sistema

#### 1. **FastAPI como Backend**

O FastAPI foi selecionado como o framework principal devido à sua velocidade, simplicidade e compatibilidade com Python. A API desenvolvida oferece endpoints para a criação, atualização, exclusão e visualização de coleções de chapéus, assegurando uma interação eficiente e segura com o banco de dados.

### Endpoints Implementados

#### **Coleções**

- `POST /collections/create/`: Criação de novas coleções de chapéus.
- `PATCH /collections/{collection_id}`: Atualização de coleções existentes.
- `DELETE /collections/{collection_id}`: Exclusão de coleções específicas.
- `GET /collections/get_all/`: Recuperação de todas as coleções disponíveis.

#### **Chapéus**

- `POST /hats/create/`: Criação de novos chapéus.
- `PATCH /hats/{hat_id}`: Atualização de chapéus existentes.
- `DELETE /hats/{hat_id}`: Exclusão de chapéus específicos.
- `GET /hats/get_all/`: Recuperação de todos os chapéus disponíveis.
- `GET /hats/collection/{collection_id}`: Recuperação de chapéus por coleção específica.

#### 2. **MongoDB como Banco de Dados**

O MongoDB foi escolhido para armazenar os dados das coleções de chapéus. Sua estrutura flexível de documentos permite escalabilidade e adaptação rápida às mudanças nos requisitos de negócios.

- **Modelo de Dados**:
  - Cada coleção de chapéus é armazenada como um documento em uma coleção do MongoDB, contendo informações como `nome_colecao`, `descricao`, `preco`, `tamanho`, `cores_disponiveis`, entre outros.

#### 3. **Segurança e Auditoria**

O projeto inclui um sistema básico de autenticação para proteger os endpoints, garantindo que apenas usuários autorizados possam realizar operações críticas. Além disso, foi implementado um sistema de auditoria utilizando o módulo de logging do Python, que registra todas as operações de criação, atualização e exclusão em logs específicos.

- **Logs de Sistema**: Armazenam informações sobre operações realizadas, como criação e atualização de coleções.
- **Logs de Segurança**: Registram tentativas de acesso não autorizadas e outras operações relacionadas à segurança.

### Como Usar o Sistema

1. **Inicializar a Aplicação**:

   - Clone o repositório do projeto.
   - Instale as dependências utilizando o arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure o banco de dados MongoDB e ajuste as configurações de conexão no código, se necessário.
   - Execute a aplicação:
     ```bash
     uvicorn main:app --reload
     ```

2. **Acessar Endpoints**:

   - Utilize uma ferramenta como **Postman** ou **Insomnia** para interagir com a API. Autentique-se utilizando as credenciais configuradas para acessar os endpoints protegidos.

3. **Gerenciar Coleções de Chapéus**:

   - Use os endpoints disponíveis para criar novas coleções, atualizar informações dos produtos e gerenciar as coleções de chapéus da loja.

4. **Consultar Logs**:

   - Os logs de operações estão disponíveis no arquivo `system_audit.log`, permitindo que os administradores revisem as atividades e assegurem a segurança e a integridade do sistema.

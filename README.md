# Dopamine pessoal — compatibilidade iOS 16

Este repositório é o espaço de trabalho do **Dopamine personalizado do utilizador**, atualmente funcional no iOS 15. **A fonte de verdade é o IPA/TIPA específico guardado no MEGA e indicado pelo utilizador na conversa; nunca o substituir por outro Dopamine.**

## Objetivo fixo

- **Dispositivo-alvo:** iPhone 8 Plus (A11).
- **Sistema-alvo:** iOS 16.7.16.
- **Base:** o mesmo IPA/TIPA personalizado que funciona no iOS 15.
- **Preservação funcional pretendida:** interface e componentes originais, RootHide/gestão de aplicações (incluindo lista/blacklist), Sileo, Patcher e integração com VCam, conforme existam e sejam identificados na cópia original.
- A adaptação pode exigir alterações internas de compatibilidade/segurança; **não confundir preservação funcional com identidade binária**.
- Não criar outro projeto, motor REA, MCP, plugin, skill, coordenador ou workflow. Não mexer em outros repositórios. Não instalar nem executar no iPhone sem autorização explícita.

## Estado verificável — 28 de outubro de 2026

| Elemento | Estado |
| --- | --- |
| Repositório GitHub | Localizado, permissões de escrita verificadas; criado vazio |
| Visibilidade | **Público** — não colocar o IPA privado, nem o link integral do MEGA/chave aqui |
| Ficheiro original | Link fornecido no chat; **download indisponível nesta sessão** |
| Hash SHA-256 do IPA original | Pendente — não foram obtidos os bytes |
| Inventário dos componentes exatos | Pendente |
| Servidor REA 6.8.0 | Contactado, sem artefacto local aberto |
| Adaptação para iOS 16 | **Não iniciada; não há IPA modificado nem testes concluídos** |

## Procedimento de trabalho

1. Tornar este repositório privado antes de guardar o IPA original ou segredos. Carregar o **mesmo IPA/TIPA do MEGA** numa Release privada ou por outro canal autorizado.
2. Calcular SHA-256 e preservar a cópia original **inalterada**.
3. Inventariar o IPA: `Info.plist`, executáveis, bibliotecas, frameworks, pacotes, entitlements, assinatura, gestores e recursos.
4. Verificar o que falha especificamente em **iPhone 8 Plus / iOS 16.7.16**. Aumentar um número de versão em `Info.plist` não constitui portabilidade.
5. Utilizar código, notas e correções compatíveis como **referências técnicas**, nunca como substituição do IPA original. Criar uma versão de trabalho separada.
6. Comparar o inventário e as funcionalidades antes/depois; documentar todas as diferenças, incluindo dependências que tenham de mudar.
7. Produzir artefacto apenas depois de compilação/assinatura e testes reais em dispositivo compatível; guardar provas e resultados.

## Referências técnicas (somente para estudo)

- [Dopamine oficial (código e histórico)](https://github.com/opa334/Dopamine)
- [Dopamine RootHide (código e versões)](https://github.com/roothide/Dopamine2-roothide)
- [Compatibilidade iPhone 8 com iOS 16.7–16.7.16](https://ios.cfw.guide/get-started/iPhone-8.html)

**Nota:** há versões mais recentes de Dopamine e de Dopamine RootHide que referem suporte para iOS 16.7.16. Isso não prova que o **IPA personalizado** do utilizador já esteja compatível nem que todos os seus componentes funcionem no iOS 16.

## Regra de evidências

Nunca declarar «adaptado», «funcional», «testado» ou «certificado» sem indicar versão exata, SHA-256, alterações aplicadas, dispositivo usado e resultados verificáveis.

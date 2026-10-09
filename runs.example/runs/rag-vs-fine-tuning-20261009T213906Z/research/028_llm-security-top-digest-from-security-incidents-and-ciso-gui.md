---
source_id: S-28
url: https://adversa.ai/blog/llm-security-top-digest-from-security-incidents-and-ciso-guides-to-mitigations-and-eu-ai-act
title: 'LLM Security Top Digest: From security incidents and CISO guides to mitigations
  and EU AI Act'
author: null
published: '2024-06-03T19:34:26.000Z'
fetched: '2026-10-09T21:39:33Z'
word_count: 1845
---
# LLM Security Top Digest: From security incidents and CISO guides to mitigations and EU AI Act

*Today let us focus on the top security concerns surrounding Large Language Models. From cutting-edge security tools to emerging threats and mitigation strategies, this edition covers a wide range of topics crucial for understanding and safeguarding against LLM-related risks.* *Explore the latest research, incidents, and initiatives shaping the landscape of LLM security, and stay informed on the forefront of AI safety and protection!*


## Subscribe for the latest LLM Security news: Jailbreaks, Attacks, CISO guides, VC Reviews and more


## **Top LLM Security initiative - EU AI Act**

[The Regulation](https://www.europarl.europa.eu/doceo/document/TA-9-2024-0138_EN.pdf) is the world’s first national AI Regulation that aims to establish a unified legal framework within the European Union to regulate the development, market access, deployment, and utilization of artificial intelligence systems (AI systems). Failure to comply with this regulation may lead to fines of up to 35M Euro.  It seeks to promote the adoption of human-centric and trustworthy AI while safeguarding fundamental rights, including health, safety, and environmental protection, as outlined in the Charter of fundamental rights of the European Union.

## **Top LLM Security Incidents**

This month there are two noteworthy incidents. [The first](https://news.hitb.org/content/japanese-police-arrest-man-after-computer-viruses-created-misusing-ai) is related to computer viruses created by misusing AI. The Metropolitan Police Department on May 28 arrested a man on suspicion of creating a computer virus using interactive generative artificial intelligence in a potential ransomware threat to companies. The second incident is covered [in the post](https://thehackernews.com/2024/05/researchers-uncover-llmjacking-scheme.html). Cybersecurity researchers have uncovered a novel attack, termed “LLMjacking,” which leverages stolen cloud credentials to access and monetize cloud-hosted large language model (LLM) services by selling this access to other threat actors. The attack involves breaching systems with vulnerabilities like CVE-2021-3129, exfiltrating cloud credentials, and using tools to validate and exploit these credentials without running legitimate LLM queries. This technique allows attackers to accumulate substantial costs for the victims, potentially disrupting business operations while covertly providing access to the compromised LLM services.

## **Top LLM Security for CISO**

[This resource](https://cloudsecurityalliance.org/ai-governance-compliance-resource-links?_gl=1*1h51pts*_ga*MTI5NjkwMDQ1NS4xNzEzMjgzMzcw*_ga_5QFZSEWJHF*MTcxNDQ3MDMzNC45LjEuMTcxNDQ3MDY2Ny41OS4wLjA) by Cloud Security Alliance is about a comprehensive collection of 200+ resources related to AI governance and compliance. It provides links to various materials that can assist in navigating the regulatory and ethical landscape of AI implementation.

## **Top LLM Prompt Injection technique** 

[The Medium blog post](https://medium.com/@munnangisravya/ascii-smuggler-the-invisible-prompt-injection-d4188d2ff951) discusses the emerging threat of invisible prompt injections, which exploit Unicode tags and ASCII smuggling to manipulate AI systems without detection. The author explains how attackers can encode malicious commands that, when processed by AI models like Claude AI, perform unintended actions, such as altering outputs or modifying data. The post also highlights the potential consequences of this vulnerability, such as data theft and integrity issues, and suggests mitigation strategies like displaying Unicode tags or dropping encoded characters before they reach the language model.

## **Top LLM Security Video** 

[Watch the YouTube video](https://youtu.be/R_JIz_FMPz8?si=ociiQ4YrTjRp--Yh) related to adversarial attacks on LLM. Very detailed video on everything you wanted to know about Jailbreaks, Prompt injections and other attacks and especially defenses for LLM.

## **Top LLM Security threat model**

[This comprehensive study](https://assets.publishing.service.gov.uk/media/664333b1ae748c43d3793a40/Cyber_security_risks_to_artificial_intelligence.pdf) by UK Government identified and mapped AI-specific vulnerabilities during the design, development, deployment, and maintenance phases, integrating insights from academic and industry literature, and expert interviews. The report also highlighted real-world and theoretical case studies, emphasizing the necessity for a holistic approach to mitigate AI-related cybersecurity risks and enhance organizational resilience against evolving threats.

## **Top LLM Security scientific paper**

[The research](https://www.anthropic.com/news/mapping-mind-language-model) by Anthropis is intended to understand the internal representation of concepts within a large language model, specifically Claude Sonnet. The researchers employed and scaled sparse autoencoders to extract high-quality, interpretable features from Claude 3 Sonnet, a medium-sized production model. They discovered a variety of highly abstract features, including those related to famous people, geographical entities, and type signatures in code, with many features being multilingual and multimodal. The results also indicated that these features could influence model behavior and address safety concerns like deception, sycophancy, bias, and dangerous content.

## **Top LLM Protection guide** 

[This author of this guide explores](https://github.com/Seezo-io/llm-security-101?s=35) the security aspects of Large Language Models (LLMs), discussing both offensive and defensive tools to understand and mitigate associated risks and vulnerabilities. It covers various topics including LLM vulnerabilities, the OWASP Top 10 for LLM applications, known hacks, and security recommendations, providing insights particularly useful for security enthusiasts new to LLM security. Additionally, it reviews open-source LLM security tools for bug bounty hunters and pentesters, and highlights popular defensive tools for large-scale company setups.

## **Top LLM Red Teaming article** 

[This blog post](https://www.blazeinfosec.com/post/llm-pentest-agent-hacking/) examines “Prompt Leaking” vulnerabilities and their exploitation through “Prompt Injection,” which, during an LLM pentest, enabled unauthorized system command execution via Python code injection. A detailed case study will explore the mechanics, implications, and exploitation methodology of these vulnerabilities. Before diving into specifics, it’s crucial to understand the basics of LLMs and their integration functions.

## **Top LLM Security Assessment** 

[This article](https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/) discusses the potential security risks associated with ChatGPT’s new memory feature, which allows the AI to retain information across sessions for a personalized experience. It highlights the threat of Indirect Prompt Injection, where an attacker could manipulate the AI to remember false information or delete memories. The post examines how this vulnerability can be exploited through connected apps, uploaded documents, and browsing, offering insights on protecting interactions with AI and building more secure applications.

## **Top LLM security research** 

[The research investigates](https://arxiv.org/abs/2405.08317) the security vulnerabilities of Integrated Speech and Large Language Models (SLMs) that can follow speech instructions and generate text responses. This is the first research  to explore potential adversarial attacks and jailbreaking techniques targeting these models. Despite achieving state-of-the-art performance on spoken question-answering tasks, experiments reveal the vulnerability of SLMs to adversarial perturbations and transfer attacks, with significant success rates in jailbreaking. However, the proposed countermeasures demonstrate effectiveness in reducing attack success rates.

## **Top LLM Security Framework** 

[The AI Security Framework](https://www.snowflake.com/en/resources/white-paper/snowflake-ai-security-framework/) by Snowflake explores the transformative impact of AI across various domains while emphasizing the critical importance of addressing associated security risks. It highlights the necessity for regular audits, adversarial testing, and transparent model development to safeguard against potential vulnerabilities introduced by AI systems. Snowflake’s AI Security Framework offers insights into potential threats, their impacts, and proposed mitigations, empowering organizations to enhance the security of their AI deployments.

## **Top LLM Security Guide**

NIST [has released four guides](https://www.csoonline.com/article/2097119/nist-publishes-new-guides-on-ai-risk-for-developers-and-cisos.html) aimed at AI developers and cybersecurity professionals, providing in-depth insights into the risks outlined in its influential 2023 “AI Risk Management Framework.” These documents address concerns such as generative AI and LLM risks, malicious training data, and synthetic content risks, offering recommendations for mitigating these threats. While not mandatory regulations, these guides are expected to become important references, setting clear boundaries for best practices in AI security, although their assimilation alongside existing cybersecurity frameworks may pose challenges for professionals.

## **Top LLM Security 101** 

This video presentation titled [“Demystifying LLMs and Threats”](https://youtu.be/8Jw6qnFnAIA?feature=shared) offers a comprehensive exploration of Large Language Models (LLMs), covering basic concepts to advanced deployment strategies in an enterprise context. Viewers will gain insights into potential threats like prompt injection and data poisoning, along with innovative defense mechanisms such as LLM firewalls and the dual LLM model. Aimed at CISOs, security professionals, and AI enthusiasts, the talk aims to enhance understanding of AI’s transformative potential and the critical security measures necessary for safe deployment in today’s digital landscape.

## **Top LLM Security VC review** 

[This review](https://www.daphni.com/insights/securing-tomorrow-ai-safety-and-ai-augmented-cybersecurity/) by Daphni VC relates to the relationship between Generative AI, particularly LLMs and cybersecurity, exploring both the potential security threats and opportunities for enhanced cyber resilience. It underscores the rapid adoption of Generative AI in various sectors and the accompanying concerns regarding privacy and security. The author discusses how GenAI can be leveraged by both cyber offenders and security practitioners, emphasizing the importance of securing its usage and promoting safe implementation to drive stronger adoption and controlled usage in corporate environments.

## **Top LLM Hacking game**

[This game](https://application.security/free/llm) is a web-based security simulation and training platform acquired by Security Compass from Kontra in 2024. the game offers immersive training experiences aimed at enhancing participants’ understanding of LLM Security and demonstrates some LLM atatcks.

## **Top LLM Security Job** 

[This AI Security engineer  job at Google](https://www.google.com/about/careers/applications/jobs/results/121150957336568518) offers the opportunity to develop technologies that shape how billions of users engage with information and each other. Responsibilities involve developing processes and infrastructure, planning and executing team exercises targeting Machine Learning deployments, designing tools and controls for defense against attackers, and effectively communicating results to various stakeholders.

## **Top LLM Safety research** 

[This paper introduces](https://arxiv.org/abs/2405.06624) a family of approaches to AI safety called guaranteed safe (GS) AI, which aims to ensure that AI systems have high-assurance quantitative safety guarantees, particularly in contexts where autonomy and general intelligence are prevalent or in safety-critical applications. The core components of GS AI include a world model, a safety specification, and a verifier, which work together to provide auditable proof certificates ensuring that the AI system satisfies the safety specification relative to its impact on the external world. The paper outlines various approaches for developing these core components, discusses technical challenges, proposes potential solutions, and argues for the necessity of this approach in AI safety.

## **Top LLM Jailbreak protection research** 

[This resource](https://www.robustintelligence.com/blog-posts/fine-tuning-llms-breaks-their-safety-and-security-alignment) considers the risks associated with fine-tuning Large Language Models (LLMs) and the potential implications for safety and security. By examining the impact of fine-tuning on model alignment and susceptibility to jailbreak instructions, the study reveals significant disparities between the original foundation model and fine-tuned variants. The findings underscore the importance of robust model testing, continuous validation, and the implementation of independent safety and security measures to mitigate risks introduced by fine-tuning in AI applications.

## **Top LLM Prompt Injection protection** 

[This repository](https://github.com/tldrsec/prompt-injection-defenses?s=35) gathers and consolidates practical and suggested defenses aimed at mitigating prompt injection vulnerabilities. While this is obviously not the full list its a good starting point into this topic.

## **Top LLM Jailbreak**

The first jailbreak is demonstrated [in the video](https://youtu.be/aqSW8wszRt4?si=syAlMkcp2wmbzmbV). It shows how to jailbreak OpenAI’s GPT-40 model and gain full control over its behavior using only an uploaded image, employing steganography and prompt injection techniques with the file name.  The second jailbreak case is featured [in the X post](https://x.com/elder_plinius/status/1791553801305952295). It describes a short and effective jailbreak method that involves converting all text to “leet speak” (a form of internet slang) and then converting it back, which reportedly works on various chat interfaces powered by different language models, including those from OpenAI, Anthropic, Google, and Meta. It notes that while the method may require several attempts on some models, it is an efficient technique.

## **Top LLM Security Report** 

[This report](https://www.immersivelabs.com/media/uploads/2024/05/Study_Dark_Side_of_GenAI.pdf) examines prompt injection techniques focused on data exfiltration targeting chatbots, emphasizing their serious threat to organizations and advocating for collaboration between the public and private sectors to address this issue, while also offering essential insights and strategies for risk mitigation. GenAI advancements are predicted to escalate cyber attacks in both frequency and severity, empowering threat actors to exploit reconnaissance and social engineering tactics with greater efficiency.  

## Be the first who will know about the latest GPT-4 Jailbreaks and other AI attacks and vulnerabilities

LLM Security Top Digest: From security incidents and CISO guides to mitigations and EU AI Act

June 3, 2024

2024LLM SecurityReviewLLM Security Digest

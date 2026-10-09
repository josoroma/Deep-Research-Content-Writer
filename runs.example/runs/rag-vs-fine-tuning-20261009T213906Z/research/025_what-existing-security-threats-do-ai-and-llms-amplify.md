---
source_id: S-25
url: https://www.mend.io/blog/what-existing-security-threats-do-ai-and-llms-amplify-what-can-we-do-about-them
title: What Existing Security Threats Do AI And LLMs Amplify?
author: Maciej Mensfeld Principal Product Architect
published: '2024-01-18T21:49:41+00:00'
fetched: '2026-10-09T21:39:33Z'
word_count: 1197
---
# What Existing Security Threats Do AI And LLMs Amplify?

In my [previous blog post,](https://www.mend.io/blog/what-new-security-threats-arise-from-the-boom-in-ai-and-llms/) we saw how the growth of generative AI and Large Language Models has created a new set of challenges and threats to cybersecurity. However, it’s not just new issues that we need to be concerned about. The scope and capabilities of this technology and the volume of the components that it handles can exacerbate [existing cybersecurity challenges](https://www.mend.io/blog/the-new-era-of-ai-powered-application-security-part-two-ai-security-vulnerability-and-risk/). That’s because LLMs are deployed globally, and their impact is widespread. They can rapidly produce a huge volume of malicious content that can influence millions within hours, and have major detrimental effects. As they rely on vast datasets and computational resources, the threats they face can be multifaceted and challenging to address. 

Let’s take a look at some pre-existing security issues that generative AI and LLMs could amplify and then consider what tactics and tools might be used to protect users against these threats.

## **Amplified existing cybersecurity threats**

- **Software vulnerabilities.** Because LLMs are just engines that run in a software ecosystem containing vulnerabilities and bugs, they may be vulnerable to regular attacks. Furthermore, malicious code and exploits can be generated using LLMs.
- **Dependency risks.** The same dynamic applies to dependency risks in generative AI and LLMs. When they rely on third-party software, libraries, or components, vulnerabilities in these dependencies can indirectly compromise the LLM.
- **Phishing and social engineering.** As with all online platforms, there’s the risk of phishing attacks aimed at gaining unauthorized access. This can occur in two ways. Firstly, you can use LLMs to craft really good phishing data. You can fine-tune data on a given person or entity based on information about their interests or behavior to craft highly targeted phishing attacks, or you can manipulate prompts that skew outcomes for social engineering purposes. In this case, LLMs aren’t the target but the tool for deception.
- **Physical security threats.** Servers and infrastructure housing the LLM can be vulnerable to physical breaches or sabotage.
- **Legal threats.** The use and abuse of copyrights could be a significant challenge when using AI and LLMs. Courts may rule that the outcome of using an AI model can’t be considered something that you can copyright, because it’s machine generated. There is no human “owner.” This could be problematic with code and creative work. Major organizations like AWS and Microsoft are investing in ways to overcome this issue by owning the whole supply chain, so they will be less dependent on third-party vendors and will have more control over the means of production and over the content itself.

Licenses are a particular legal issue when considering the outcomes of using LLMs. For example, if you don’t realize that an original source in your LLM isn’t permissive, then you could face legal action for using it. There’s a gray area where the LLM outcome may resemble a piece of code that is licensed under a copyleft license with certain requirements, such as the Apache 2 license with a commons clause. If the outcome is then adopted and used by somebody else, then you could both be sued, in theory, for not applying the proper license criteria. You could be forced to stop using this piece of code and replace it with something else or pay millions.

On the other hand, AI and LLMs can make it more difficult to claim ownership and assert licensing rights, because an element of machine generation has been injected into the mix. If your LLM generates 20 lines of generic code that sits within hundreds more lines of code, who owns it if someone else fine-tunes it? There will be some open projects where you give an LLM a description of what you want to build, and it’ll create multiple functions from numerous bits of code. Who owns what is generated? This problem is why some companies don’t allow developers to use public LLMs, or impose restrictions on their use.

## **How to secure generative AI and LLMs**

What can you do to maintain security when using generative AI and LLMs? Strategies and tactics include:

- **Fine-tuning.** This involves calibrating the LLM on custom datasets to restrict or guide its behavior. In theory, this will set your model in the right direction and steer it away from generating less accurate and more unexpected information and data. By taking care to do this, you guide your LLM towards generating more expected results, which you can be more confident are reliable. Does it always work? Probably not. Does it generally work? Yes, because you are providing guard rails for the LLM from which they shouldn’t deviate.
- **Input filtering.** Similarly, this is about instructing or guiding your LLM to better meet your needs and avoid any unexpected behaviors. Input filtering uses algorithms to filter out harmful or inappropriate prompts. It’s a methodology that a few companies are working on, alongside output filtering, as a way to stop generating code that could be damaging to you and your customers. Use logging and monitoring tools like Splunk or ELK Stack to analyze logs for signs of misuse.
- **Rate limiting** . We’ve previously noted that the volume, speed, and complexity of AI and LLMs present a threat because the vast number of inputs and data means it’s easy to overlook some issues. To prevent abuse, you can limit the number of requests a user can make within a specific time frame. Apply tools such as web application firewalls (WAF) to protect LLM API endpoints from common web-based attacks.
- **Continuous monitoring and auditing.** At Mend.io, we are big advocates for making security a constant and ongoing process. Applying this as best practice and instilling it as a mindset within your organization will certainly harden your cybersecurity. When it comes to these new tools and technologies, constantly evaluating the outputs and behaviors of the LLM for any signs of misuse or unexpected behavior, means you’re alert to them and can address them quickly, before they cause damage or before their impact can escalate.
- **Intrusion detection systems (IDS).** These enable you to monitor and detect malicious activities.
- **User authentication.** Ensure that only authenticated users can access the LLM by deploying authentication systems like OAuth or JWT.

We can anticipate that new methods and tools will emerge to secure generative AI and LLMs, such as advanced behavior analysis**,** which will use AI to monitor and understand the behavior of users interacting with the LLM, and decentralized LLMs, which involves deploying LLMs in decentralized networks to reduce single points of failure in a similar vein. We can also anticipate the development and introduction of decentralized security protocols: distributed systems that can secure LLMs without relying on central authorities.

AI will also be deployed in securing itself with self-adapting security systems – security tools driven by AI that can adapt in real time to emerging threats. Blockchain could be used for auditing by providing immutable records of all interactions with the LLM for traceability. And there’ll be a role for semantic analyzers, to analyze the content generated by LLMs so that it meets ethical and safety guidelines.

Whatever the direction generative AI and LLMs takes, one thing you can be sure of is that as the technology evolves and becomes even more sophisticated, security methodology must also develop further.

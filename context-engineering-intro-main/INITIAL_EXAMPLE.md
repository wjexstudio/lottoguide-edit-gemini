## FEATURE:

- Pydantic AI agent that has another Pydantic AI agent as a tool.
- Research Agent for the primary agent and then an email draft Agent for the subagent.
- CLI to interact with the agent.
- Gmail for the email draft agent, Brave API for the research agent.

## EXAMPLES:

In the `examples/` folder, there is a README for you to read to understand what the example is all about and also how to structure your own README when you create documentation for the above feature.

- `examples/cli.py` - use this as a template to create the CLI
- `examples/agent/` - read through all of the files here to understand best practices for creating Pydantic AI agents that support different providers and LLMs, handling agent dependencies, and adding tools to the agent.

Don't copy any of these examples directly, it is for a different project entirely. But use this as inspiration and for best practices.

## DOCUMENTATION:

Pydantic AI documentation: https://ai.pydantic.dev/

## OTHER CONSIDERATIONS:

- Include a .env.example, README with instructions for setup including how to configure Gmail and Brave.
- Include the project structure in the README.
- Virtual environment has already been set up with the necessary dependencies.
- Use python_dotenv and load_env() for environment variables

<!--

## คุณสมบัติ:

-ตัวแทน Pydantic AI ที่มีตัวแทน Pydantic AI อื่นเป็นเครื่องมือ
-ตัวแทนการวิจัยสำหรับตัวแทนหลัก จากนั้นจึงร่างตัวแทนอีเมลสำหรับตัวแทนย่อย
-CLI เพื่อโต้ตอบกับตัวแทน
-Gmail สำหรับตัวแทนร่างอีเมล, Brave API สำหรับตัวแทนการวิจัย

## ตัวอย่าง:

ในโฟลเดอร์ `examples/` มี README ให้คุณอ่านเพื่อทำความเข้าใจว่าตัวอย่างนี้เกี่ยวกับอะไร และรวมถึงวิธีจัดโครงสร้าง README ของคุณเองเมื่อคุณสร้างเอกสารประกอบสำหรับคุณสมบัติข้างต้น
-`examples/cli.py` -ใช้สิ่งนี้เป็นเทมเพลตเพื่อสร้าง CLI
-`ตัวอย่าง/ตัวแทน/` -อ่านไฟล์ทั้งหมดที่นี่เพื่อทำความเข้าใจแนวปฏิบัติที่ดีที่สุดสำหรับการสร้างตัวแทน Pydantic AI ที่รองรับผู้ให้บริการและ LLM ที่แตกต่างกัน การจัดการการพึ่งพาตัวแทน และการเพิ่มเครื่องมือให้กับตัวแทน

อย่าคัดลอกตัวอย่างใดๆ เหล่านี้โดยตรง เนื่องจากเป็นการคัดลอกสำหรับโปรเจ็กต์อื่นโดยสิ้นเชิง แต่ใช้สิ่งนี้เป็นแรงบันดาลใจและแนวทางปฏิบัติที่ดีที่สุด

## เอกสาร:

เอกสาร Pydantic AI: https://ai.pydantic.dev/

## ข้อควรพิจารณาอื่นๆ:

-รวม .env.example, README พร้อมคำแนะนำในการตั้งค่า รวมถึงวิธีกำหนดค่า Gmail และ Brave
-รวมโครงสร้างโครงการไว้ใน README
-สภาพแวดล้อมเสมือนจริงได้รับการตั้งค่าพร้อมการขึ้นต่อกันที่จำเป็นแล้ว
-ใช้ python_dotenv และ load_env() สำหรับตัวแปรสภาพแวดล้อม

-->
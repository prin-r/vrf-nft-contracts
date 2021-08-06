import pytest
from brownie import accounts, Bridge, StdReferenceBasic, StdReference

# Returns the POA mainnet validator set
@pytest.fixture(scope="module")
def testnet_validator_set():
    return [
        ["0xacD0D2294551276ecb23bC8761194883cBC52d56", "199982"],
        ["0x292647a34C47b1d5b4edaF12aFCC2886FDa9Ac52", "202826"],
        ["0x9C6c1C75e9517aAB924816D97fDa00A495A11247", "200103"],
        ["0xb3fcDF9be8647c73201f21ea6D26BAf4Dd868DC6", "202920"],
        ["0x0188DE5D539f89Ab9fE1F4632fEa5D4742BE2D05", "201167"],
        ["0x5d0D8D9B5B4bBfB6B24110925278fc317477Fe92", "200103"],
        ["0x3aF6961634E70D2Ce370486A611023c5a260e1f2", "200003"],
        ["0x58e22F35D79b5472BbcDA764915Cae30D9d40172", "199982"],
        ["0x9698a854F9ac6d54adB173Da2fA4E1973FfaEA10", "200103"],
        ["0xc2C62106baE6600B11D53a142260a62283BF47e6", "400007"],
        ["0xFe4906FD7BfB1d7D8843Cad1445e8AF13Ed79822", "200062"],
        ["0x2bCFAd5Ec2E72bD70C027D74C395Be27F94CBA4E", "200003"],
        ["0x88f6cCCc77C64D1993dfA3C654A145Dd1420696B", "202593"],
        ["0xA4520fDE4d5800774fba4A508D53b542B84CC932", "200003"],
        ["0x05e046D52F0D65CfB2672C8E0a56fe6C4f698785", "200003"],
        ["0x0fBE5d4C73Be0ba5139F75a0222403BdB3Bc44bf", "9"],
        ["0x8C7c14239fFCd0262a86909C33ae7C7Ad4dfF2bB", "200003"],
        ["0x3c111D1f2A9f5282Bba63330C9b0E89567314210", "200003"],
        ["0x7c7f874e56Ec26af1E856Edb978C6b039369Ae80", "200062"],
        ["0x492Eda9cA00bf58F390B87044ac0C671D36455E2", "200003"],
        ["0x13150B6A4435d8AA40b5Be6b086FAD9Fa7645CC6", "200003"],
        ["0xab57ad6997d1D7e016ac6bac69f01cFFD17D4e16", "200003"],
        ["0xc50982A35152B072ec480c34A257791fcd26C16E", "200003"],
        ["0x9CB2F9337A06a4EbbB9E4986C4569A7365b75dcA", "200009"],
        ["0x4fcc913cc25829A7A915650D71fCA0CcD36F5f00", "3800501"],
        ["0x2D60D1cBAB562c4DA98c2a4BC6dBeDF962Ea5d99", "200003"],
        ["0xc9aDdBfa5d815208b3050f0B8aecF26826232c6B", "200108"],
        ["0x93C3707F02cd28630aafd61811712bC0C8228510", "200003"],
        ["0xe906EDB9Ae29d6c8449b45818EAD3295c520A5BB", "200535"],
    ]


@pytest.fixture(scope="module")
def testnet_aggregator_proof():
    return "0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000172000000000000000000000000000000000000000000000000000000000000016c0000000000000000000000000000000000000000000000000000000000018eebafced3cf3c7f9a288c496c122fb79545a5248ae4a89cf18a1b8062d7da19e149a87ae99c9a004eeffebe57e25dc062fde161e8d2d14e3b4fb3c5ab5cb6caa3e5e7b1b2fcaab8a0c71dfdd07c0da6f330c0c611e7398e4d91d48eb206f8c5b839f9c3619ffc762ed94f1c71e82c5ec1ae0c7373554b69d847db73703c18ff761d52afda879cd257ba5ab58d8672900c8b1ac584fb5f098855da7c68ddb93c717694fa9ca1048d3f4baa282c89c96bd4259c5bbfdf9839215502b59f40c37d3b8b4571fecd391d98be0271a63a50976b387c434228d5a2a02ee5d652d45ffb7ba7432438a854607b9b060fea33eaa4853fc6bf98251b71a2138b897a2441063dae6de470f4af1a25c56c25f74fe4ce1999252350be907a9334cf686b983d349b334349a76e7bedd40bbf888f7726a24f75ef5c71591629dbe3eef272c94db4a2d66f7be5f653d1d216398666bf617be22066ca3196b60c7d614aa981a4a93237cef00000000000000000000000000000000000000000000000000000000000001a0000000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000320000000000000000000000000000000000000000000000000000000000000048000000000000000000000000000000000000000000000000000000000000005e0000000000000000000000000000000000000000000000000000000000000074000000000000000000000000000000000000000000000000000000000000008a00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000b600000000000000000000000000000000000000000000000000000000000000cc00000000000000000000000000000000000000000000000000000000000000e200000000000000000000000000000000000000000000000000000000000000f8000000000000000000000000000000000000000000000000000000000000010e0000000000000000000000000000000000000000000000000000000000000124000000000000000000000000000000000000000000000000000000000000013a060dafab2e14ea8b9886183a43eb0f4171caaf1df7d65fb813bbfd51c0a47d026316f9f9237649299ae6962cdde741170aeda90905cbd03ff1393db161861e096000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510e3f6e3d401321462616e642d6775616e79752d746573746e657433000000000000000000000000000000000000000000009170af33bc67f7d41afe355898567829e884d1ace697bc4b594dd4f2750ebeed2b246b2e93a63459b74bf6472b1159d6534bab3a2706f9a515db4a36b8d19d98000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd05108ffff8a201321462616e642d6775616e79752d746573746e657433000000000000000000000000000000000000000000005b0c5df6191a7d032c110f5054f29dea422d15d4a09e70dcef20f36bd026fbdb02ebf4751bf6af4414ecca215d0a72efbcb8f512d82299642641f1da0e02d92c000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd05109ca7dbd301321462616e642d6775616e79752d746573746e657433000000000000000000000000000000000000000000003e44a1062ab9b655adf20fb7929f5f0f75a7c0c6985ccf46d0d6c7477a238949734a39aa35398c3862357ac69bb2b37bb2885c3a9dffc250131e2d9bf0a94228000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd051082f8dcdf01321462616e642d6775616e79752d746573746e65743300000000000000000000000000000000000000000000c4659670c1d2802e3194c9c817f9d6373211e2cbae56d70d4edb47e43cf89039546eb24456a40091237568bac9eabbd6446e7a3c67171fb9a08636eb9c9a10dc000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510e3bce8d001321462616e642d6775616e79752d746573746e657433000000000000000000000000000000000000000000003f1d77892e8ddbe9f422254f47b726d639d64483ae8bd9d666127c426e7fac156bda545fdb231afe0d8e75aa160c2ceaabe23c066157b56b7579010d6170e19e000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd05109ffee0b701321462616e642d6775616e79752d746573746e65743300000000000000000000000000000000000000000000f2cb49efbdac0449cdd47a26e37be98d61715555decb24115e8d1499daeb78972e004e5d8d671c79554b15fba463ada257453768ab44d08199399081414ea52e000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510c1a480dd01321462616e642d6775616e79752d746573746e657433000000000000000000000000000000000000000000003847c3697292a75f5c85e18777aa3a7416081e52c50c0b5c54816aaa4e0ccc3a746dc8054b9cf25e82227c1fa240af05334cc416c90bb90a1e8e437c18324414000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd05108a89e3ae01321462616e642d6775616e79752d746573746e65743300000000000000000000000000000000000000000000d2b18c47be0d79c7a52445831b98b3799aa5c18bb9c515cc1f1302d4d8332a9e1ad5b137037c979b4a20ebd0bd256774eda14912da4f79bacb4b4d8297e25ca4000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510e585e99d01321462616e642d6775616e79752d746573746e6574330000000000000000000000000000000000000000000006183abe0db54fc70d9cf15fc1c5816f0701523125bc5af79b039d45aad1806c1d8e866bc394220fbb6df815fb7cd4b5d5b805769ebfe321669d4d6947487cb8000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510f8dcded801321462616e642d6775616e79752d746573746e6574330000000000000000000000000000000000000000000098fce06b0b47985b5b7d43b1323525f30d6af070d1fbd4d4e55db75afcb3a62350e41eb12cbbfc0955cb3cebee4b7c9c4b3fdedfbbe72162f7787240d17471ba000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510d89ba0dc01321462616e642d6775616e79752d746573746e6574330000000000000000000000000000000000000000000073e4dcffb30dfbda4e4ccacd95f670bc3261bbc1ef73e44f7165211a8491509d17d2d89f30a4b9920b69adf167d71d7da9329222bf3ec940d73003efa253a8c9000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510d1d7d1cc01321462616e642d6775616e79752d746573746e65743300000000000000000000000000000000000000000000638602e7467b1bf7c09c8de790e02e6fb48e0c48b77881f2aee529967fe19f323e3b5f7511a40eb83dc44a74c02b1baed7c124adc6477b499f1102ebbf826610000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510a583d2d201321462616e642d6775616e79752d746573746e65743300000000000000000000000000000000000000000000503009a970aa12c6691386bc276e91c00d4c1d57c8b89d110e572bad35f93a42722624ee5b65e50898e23272f3b7ce94111de6bc394e49aefb2f2018d0ec81cf000000000000000000000000000000000000000000000000000000000000001b00000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000001079080211baee18000000000022480a2000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004a12240a20900cede24daf9a11846ab90a219a0250af3da10d538682bcd6e68cea327f680310012a0c08f5f8aafd0510dfc6c4b901321462616e642d6775616e79752d746573746e6574330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000012c0000000000000000000000000000000000000000000000000000000000018eeba00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000018eeb900000000000000000000000000000000000000000000000000000000000003a000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000000000000000000000000000000900000000000000000000000000000000000000000000000000000000000000e00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000862616e647465616d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000540000000a0000000342544300000003455448000000045553445400000003585250000000044c494e4b00000003444f5400000003424348000000034c54430000000341444100000003425356000000003b9aca0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000004d2a1000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000005faabc65000000000000000000000000000000000000000000000000000000005faabc6f00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000000862616e647465616d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000540000000a00000dd76a25ec8000000067c1059500000000003b9aca00000000000f23be9500000002faf1435000000001036be5500000003bffdd176f0000000d737014a000000000063f7495000000249b84e3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000018eeb96a594a2c7f3e4763deca7d49b50e083862d223a17a4c183365a2a97fc17c3373000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000018eeb9dacfea3293562b3c6f25878904e7fd8fc2dfd7267beb111a8021bce3729eb933000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000005000000000000000000000000000000000000000000000000000000000018eeb9c316ed8488dcd6110fb2b592b60eb56760364d974c92aba0ad56611d404eb63300000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000d000000000000000000000000000000000000000000000000000000000018eeb99029908b6f79d774d5b7529a4af3c6f1b134864565c206751c414825a0b6ffcd00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000005000000000000000000000000000000000000000000000000000000000000001d000000000000000000000000000000000000000000000000000000000018eeb971b7b3baf5874ccb075d46cde25ea88f42f1917e654999e5546ee2a624b2cb0600000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000003d000000000000000000000000000000000000000000000000000000000018eeb9c7d13df3027a349bd5cd5d677fffdbd084c2786f26fd9261d106c2e2d9e021d700000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000007000000000000000000000000000000000000000000000000000000000000005d000000000000000000000000000000000000000000000000000000000018eeb9dcabf0d1b379669e97493f12055de7143152acef84f8e1a5cfd0570eba0328a900000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000009d000000000000000000000000000000000000000000000000000000000018eeb94a48b02149d9a3a412a1c30ea70e89c22907b1bde7d4ce42fa10150480f7afda00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000009000000000000000000000000000000000000000000000000000000000000019d000000000000000000000000000000000000000000000000000000000018eeb9f17e2462d4647e1cea98f2373c49ed23303c57a677c433e683cb9c580cd4ba430000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000039d000000000000000000000000000000000000000000000000000000000018eeb9390b180691ea83c310935c70bcfc8f56cfd8d502057cca1536cdb3fce1d95da50000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000b000000000000000000000000000000000000000000000000000000000000059d000000000000000000000000000000000000000000000000000000000018eeb9ef7f0cd38964c7cfaa37c5a65a409e8408f36f581d4e8e1faf849f2a35ba04b70000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000d9d000000000000000000000000000000000000000000000000000000000018eeb9bfbd4cfeaf2d191928898a6546648ff9269a7108440c2237913f9ea0b0fdea220000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000d0000000000000000000000000000000000000000000000000000000000001d9d000000000000000000000000000000000000000000000000000000000018eeb91abb42c967afa96a75983dbff8681d883de6ed924e8e5bc91c343017a2633d570000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000003d9d000000000000000000000000000000000000000000000000000000000018eeb9b81938e1acb7acfce8048d781ad65b1b39452ce04bfa7d6380f3e33bfdd917620000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000f0000000000000000000000000000000000000000000000000000000000005d9c000000000000000000000000000000000000000000000000000000000018eeb977d465cfad31526ec66239cab8eabad78d4f380d009cd35f019c20c38c12089c00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000d1d7000000000000000000000000000000000000000000000000000000000018eeb96fb38d3e2fbff070532550ca5723484dfdf237817f3606ab21eef0890a7ad2770000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001100000000000000000000000000000000000000000000000000000000000197b4000000000000000000000000000000000000000000000000000000000018eeb923dd23dca90864dc64b7f1e4b0cc2b0eea9020147d2a5c3d69da68a01af2d164000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000025b7c000000000000000000000000000000000000000000000000000000000018eeb96d1a8f32ccea57372cb54d735d9e6b62cdf298122e5c124d22387fb990abf57e00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000013000000000000000000000000000000000000000000000000000000000004d39d000000000000000000000000000000000000000000000000000000000018eeb9cdfe3cdabe9dd9fcacfbceb5748b4aac330ba4f44a85255892814e4237903f9f0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001500000000000000000000000000000000000000000000000000000000000b9f10000000000000000000000000000000000000000000000000000000000018eeb983170ccb781e8f0c2a842c5ec8b474369dc1815ed930da25723462ebe3612fbf0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001600000000000000000000000000000000000000000000000000000000001608a4000000000000000000000000000000000000000000000000000000000018eeb9c6dbb6f6b858f50b8c6867a19fabc4164a0baa9081d928a672ac4b0bd58c485f0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000001700000000000000000000000000000000000000000000000000000000001feb53000000000000000000000000000000000000000000000000000000000018eeb91a101696357c0dbc43fe425a03046c37efe1bf77480e1a39e2b610df31b1b6a500000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000018000000000000000000000000000000000000000000000000000000000032de65000000000000000000000000000000000000000000000000000000000018eeb94777870c1514e8f0a337d2a0ee79b50aa46186b8fc56d01a8165ce4ce021bcec000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000190000000000000000000000000000000000000000000000000000000000563e10000000000000000000000000000000000000000000000000000000000018eeb9a03813903fc12ea7c2904643552747e87e1855bea83063ddf453ea00856d1156"


# Deploy StdReferenceBasic contract
@pytest.fixture(scope="module")
def stdrefbasic():
    return accounts[0].deploy(StdReferenceBasic)


# Deploy StdReferenceBasic contract
@pytest.fixture(scope="module")
def stdrefbasicv2(testnet_validator_set):
    bridge = accounts[0].deploy(Bridge, testnet_validator_set)
    return accounts[0].deploy(StdReference, bridge, [9], 10, 5)